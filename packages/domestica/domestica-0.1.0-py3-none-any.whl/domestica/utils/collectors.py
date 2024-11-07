import asyncio
import json
import re
from typing import Optional

from playwright.async_api import BrowserContext, Page

from .. import helpers
from ..models import Course, CourseInfo, Media, Section, Video
from ..utils import tools


def get_course_id(url: str) -> str:
    pattern = r"/(\d+)-"
    match = re.search(pattern, url)
    if not match:
        raise Exception("Could not get course id")
    return match.group(1)


def _parse_course_info(content: str) -> CourseInfo:
    pattern = r"window\.Domestika\.courses_controller\.course\((.*?)\);"
    match = re.search(pattern, content)
    if not match:
        raise Exception("Could not get course info")
    try:
        json_str = match.group(1)
        json_data = json.loads(json_str)
        json_info = json_data["amplitude_event"]["event_properties"][
            "product_attributes"
        ][0]
        return CourseInfo(**json_info)
    except Exception as e:
        raise Exception("Could not parse course info") from e


async def fetch_course_info(url: str, context: BrowserContext) -> CourseInfo:
    page = await context.new_page()
    await page.goto(url)
    return _parse_course_info(await page.content())


async def get_course_title(page: Page) -> str:
    try:
        title = await page.locator("h1.course-header-new__title a").text_content()
    except TimeoutError:
        raise Exception("Could not get course title")

    if title is None:
        raise Exception("Could not get course title")
    return helpers.clean_string(title)


async def page_to_img(page: Page, path: Optional[str] = None) -> bytes:
    await page.emulate_media(media="screen")
    return await page.screenshot(path=path, full_page=True)


async def page_to_pdf(page: Page, path: Optional[str] = None) -> bytes:
    await page.emulate_media(media="screen")
    return await page.pdf(path=path)


async def _exit_multi_courses(page: Page) -> None:
    multi_courses_locator = page.locator(".a-tag.bg-color-guijarro")
    if await multi_courses_locator.count() > 0:
        await page.close()
        raise Exception("This kind of course is not supported")


async def fetch_course(url: str, context: BrowserContext) -> Course:
    page = await context.new_page()
    await page.goto(url)

    await _exit_multi_courses(page)

    title = await get_course_title(page)

    try:
        tasks = []
        sections: list[Section] = []
        sections_locator = page.locator("ul.units-list h4.unit-item__title a")
        for i in range(await sections_locator.count()):
            section_url = await sections_locator.nth(i).get_attribute("href")
            if section_url is None:
                raise Exception("Could not get section url")
            tasks.append(fetch_section(section_url, context))
        sections = await asyncio.gather(*tasks)
    except TimeoutError:
        await page.close()
        raise Exception("Could not get sections")
    except Exception as e:
        await page.close()
        raise e

    # Capture content as PDF
    pdf_content_url = await tools.upload_from_bytes(
        await page_to_pdf(page),
        f"{title}_content.pdf",
    )

    info = _parse_course_info(await page.content())

    await page.close()

    return Course(
        id=get_course_id(url),
        title=title,
        url=url,
        sections=sections,
        assets=[
            Media(name="content", url=pdf_content_url),
        ],
        info=info,
    )


async def fetch_section(url: str, context: BrowserContext) -> Section:
    page = await context.new_page()
    await page.goto(url)

    # TODO: implement this
    if url.endswith("/final_project"):
        await page.close()
        return Section(
            title="Final Project",
            videos=[],
            assets=[],
        )
    try:
        section_title = await page.locator("header.paper__header h2").text_content()
    except TimeoutError:
        await page.close()
        raise Exception("Could not get section title")

    if section_title is None:
        await page.close()
        raise Exception("Could not get section title")

    section_title = helpers.clean_string(section_title)

    pattern = r"window\.__INITIAL_PROPS__ = JSON\.parse\('(.*?)'\)"
    match = re.search(pattern, await page.content())
    if not match:
        await page.close()
        raise Exception("Could not get section content")

    json_str = match.group(1).replace("\\", "")
    json_data = json.loads(json_str)
    videos: list[Video] = []
    try:
        for video in json_data["videos"]:
            media = Video(
                title=helpers.clean_string(video["video"]["title"]),
                m3u8_url=video["video"]["playbackURL"],
            )
            videos.append(media)
    except KeyError:
        await page.close()
        raise Exception("Could not get section videos")

    # Capture content as PDF
    pdf_content_url = await tools.upload_from_bytes(
        await page_to_pdf(page),
        f"{section_title}_content.pdf",
    )

    await page.close()

    return Section(
        title=section_title,
        videos=videos,
        assets=[
            Media(name="content", url=pdf_content_url),
        ],
    )
