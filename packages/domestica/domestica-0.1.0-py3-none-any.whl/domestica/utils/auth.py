from playwright.async_api import BrowserContext

from .. import helpers
from .appdirs import get_config_file_path


async def load_state(context: BrowserContext) -> bool:
    try:
        config_path = get_config_file_path()
        credentials = helpers.read_json(config_path)
        cookies = credentials["cookies"]
        await context.add_cookies(cookies)  # type: ignore

        page = await context.new_page()
        await page.goto("https://www.domestika.org")
        await page.wait_for_selector("span[class='avatar avatar--s']")
        return True
    except Exception:
        return False
    finally:
        await page.close()


async def login(email: str, password: str, context: BrowserContext) -> None:
    page = await context.new_page()
    await page.goto("https://www.domestika.org/auth/login")
    await page.fill("#user_email", email)
    await page.fill("#user_password", password)
    await page.click(".simple-credentials .t-login-button")

    try:
        await page.wait_for_selector("span[class='avatar avatar--s']")
    except Exception:
        raise Exception("Could not login")

    cookies = await context.cookies()
    credentials = {
        "email": email,
        "password": password,
        "cookies": cookies,
    }
    config_path = get_config_file_path()
    helpers.write_json(credentials, config_path)
