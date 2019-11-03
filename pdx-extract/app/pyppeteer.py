import pyppeteer

from app.urls import INIT_URL


async def initialize():
    """Initializes pyppeteer browser with options.

    Doesn't open or close browser, that responsibility is left to the caller.

    Returns:
        Browser: A Pyppeteer browser.
    """
    args = ["--no-sandbox", "--disable-setuid-sandbox", "--ignore-certificate-errors"]
    browser = await pyppeteer.launch(args=args, headless=True)

    return browser


async def get_page(browser):
    """ Accesses a page via the Pyppeteer browser.

    Parameters:
        Browser: A Pyppeteer browser.
    """
    page = await browser.newPage()
    await page.goto(INIT_URL)
    return page


async def get_tokens(browser):
    """Returns JSESSIONID and uniqueSessionId needed for receiving a
    successful response from HTTP requests.

    :param browser: Instantiated pyppeteer browser
    :returns: The JSESSIONID and uniqueSessionId
    """
    page = await browser.newPage()
    await page.goto(INIT_URL)

    session_id = await get_jsession_id(page)
    unique_session_id = await get_unique_session_id(page)

    return session_id, unique_session_id


async def get_jsession_id(page):
    cookies = await page.cookies(INIT_URL)
    cookies = {cookie["name"]: cookie["value"] for cookie in cookies}

    return cookies["JSESSIONID"]


async def get_unique_session_id(page):
    unique_session_id = await page.evaluate("sessionStorage.getItem(STORAGE)")

    return unique_session_id
