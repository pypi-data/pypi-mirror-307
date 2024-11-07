import asyncio
import os
from pathlib import Path

import typer
from rich.console import Console

from . import helpers
from .client import Client
from .constants import Messages
from .models import Quality
from .utils import appdirs, tools

app = typer.Typer(
    rich_markup_mode="markdown",
    epilog="Made with :heart: by [ivansaul](https://github.com/ivansaul)",
)
console = Console()


@app.command()
def login() -> None:
    """
    Authenticates a user with the given email and password.
    """
    while True:
        email = typer.prompt("What's your email?")
        confirm_email = typer.prompt("Confirm your email?")
        if email == confirm_email:
            break
        console.print(Messages.VALUE_DOES_NOT_MATCH)

    while True:
        password = typer.prompt("What's your password?", hide_input=False)
        confirm_password = typer.prompt("Confirm your password?", hide_input=False)
        if password == confirm_password:
            break
        console.print(Messages.VALUE_DOES_NOT_MATCH)

    console.print("⠹ Logging in...", style="bold green")

    try:
        asyncio.run(_login(email, password))
        console.print("✓ Logged in successfully.", style="bold green")
    except Exception as e:
        error_message = str(e)
        console.print(error_message, style="bold red")
        raise typer.Exit()


@app.command()
def logout() -> None:
    """
    Logs out the user.
    """
    appdirs.delete_app_config_file()
    console.print("✓ Logged out successfully.", style="bold green")


@app.command()
def refresh() -> None:
    """
    Refreshes the cookies of the user.
    """
    config_path: Path = Path(appdirs.get_config_file_path())
    if not config_path.is_file():
        console.print("✗ Not logged in. Please login first.", style="bold red")
        raise typer.Exit()

    try:
        credentials = helpers.read_json(config_path.as_posix())
        email = credentials["email"]
        password = credentials["password"]
    except Exception:
        console.print("✗ Not logged in. Please login first.", style="bold red")
        raise typer.Exit()

    console.print("⠹ Refreshing cookies...", style="bold green")

    try:
        asyncio.run(_login(email, password))
        console.print("✓ Cookies refreshed successfully.", style="bold green")
    except Exception as e:
        error_message = str(e)
        console.print(error_message, style="bold red")
        raise typer.Exit()


@app.command()
def download() -> None:
    """
    Downloads the course with the given URL.
    """
    url = typer.prompt("What's the URL of the course?")
    asyncio.run(_download(url))


async def _login(email: str, password: str) -> None:
    async with Client(headless=False) as client:
        await client.login(email, password)


async def _download(url: str) -> None:
    async with Client(headless=False) as client:
        # TODO: implement human verification
        await client.verify_captcha(url)

        info = await client.fetch_course_info(url)
        console.print(info.dict())

        course = await client.fetch_course(url)

        save_dir = course.title
        os.makedirs(save_dir, exist_ok=True)
        for idx, section in enumerate(course.sections, start=1):
            section_dir = os.path.join(save_dir, f"{idx:02}. {section.title}")
            os.makedirs(section_dir, exist_ok=True)

            # dl section videos
            for idx, video in enumerate(section.videos, start=1):
                await tools.download_m3u8_video(
                    url=video.m3u8_url,
                    save_dir=section_dir,
                    quality=Quality.P224,
                    subtitle_lang="en",
                    output_name=f"{idx:02}. {video.title}",
                )

            # dl section assets
            for asset in section.assets:
                output = asset.name + os.path.splitext(asset.url)[1]
                await tools.download_file(asset.url, section_dir, output)

        # dl course assets
        for asset in course.assets:
            output = asset.name + os.path.splitext(asset.url)[1]
            await tools.download_file(asset.url, save_dir, output)

        # dl course data json
        helpers.write_json(course.dict(), os.path.join(save_dir, "course.json"))
