import asyncio

from playwright.async_api import BrowserContext, Page, async_playwright

from .models import Course, CourseInfo
from .utils import appdirs, auth, collectors


class Client:
    def __init__(self, headless: bool = False):
        self.headless = headless

    async def __aenter__(self):
        self._playwright = await async_playwright().start()

        self._browser = await self._playwright.chromium.launch(headless=self.headless)
        self._context = await self._browser.new_context(
            java_script_enabled=True,
            is_mobile=True,
        )

        try:
            await self.load_state()
        except Exception:
            raise Exception("Could not load state")

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._context.close()
        await self._browser.close()
        await self._playwright.stop()

    @property
    def config_path(self) -> str:
        return appdirs.get_config_file_path()

    @property
    async def page(self) -> Page:
        return await self._context.new_page()

    @property
    def context(self) -> BrowserContext:
        return self._context

    async def verify_captcha(self, url: str) -> None:
        # TODO: improve this - human verification
        page = await self.page
        await page.goto(url)
        await asyncio.sleep(20)
        await page.close()

    async def login(self, email: str, password: str):
        await auth.login(email, password, self.context)

    async def load_state(self) -> None:
        await auth.load_state(self.context)

    async def fetch_course_info(self, url: str) -> CourseInfo:
        return await collectors.fetch_course_info(url, self.context)

    async def fetch_course(self, url: str) -> Course:
        return await collectors.fetch_course(url, self.context)
