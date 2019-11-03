import asyncio

import asynctest
import pytest

from app import pyppeteer
from tests import utils


@pytest.mark.asyncio
@asynctest.patch("pyppeteer.launch")
async def test_initialize_browser_returns_browser(mock_launch):
    mock_launch = utils.set_async_result(mock_launch, "mock-browser")

    browser = await pyppeteer.initialize()

    mock_launch.assert_called
    assert browser == "mock-browser"


@pytest.mark.asyncio
@asynctest.patch("app.pyppeteer.get_unique_session_id")
@asynctest.patch("app.pyppeteer.get_jsession_id")
@asynctest.patch("pyppeteer.page")
async def test_get_tokens_returns_session_and_unique_ids(
    mock_page, mock_jsession_id, mock_unique_id
):
    page = asynctest.CoroutineMock()
    page.goto.return_value = asyncio.Future()
    page.goto.return_value.set_result(None)
    browser = asynctest.CoroutineMock()
    browser.newPage.return_value = asyncio.Future()
    browser.newPage.return_value.set_result(page)
    mock_jsession_id = utils.set_async_result(mock_jsession_id, "test-jsession-id")
    mock_unique_id = utils.set_async_result(mock_unique_id, "test-unique-id")

    session_id, unique_session_id = await pyppeteer.get_tokens(browser)

    mock_jsession_id.assert_called
    mock_unique_id.assert_called
    assert session_id == "test-jsession-id"
    assert unique_session_id == "test-unique-id"


@pytest.mark.asyncio
@asynctest.patch("pyppeteer.page")
async def test_get_jsession_id_returns_jsession_id(mock_page):
    mock_cookies = [
        {"name": "foo", "value": "bar"},
        {"name": "baz", "value": "qux"},
        {"name": "quux", "value": "corge"},
        {"name": "JSESSIONID", "value": "test-unique-jsession-id"},
    ]
    mock_page.cookies.return_value = asyncio.Future()
    mock_page.cookies.return_value.set_result(mock_cookies)

    unique_session_id = await pyppeteer.get_jsession_id(mock_page)

    mock_page.assert_called
    assert unique_session_id == "test-unique-jsession-id"


@pytest.mark.asyncio
@asynctest.patch("pyppeteer.page")
async def test_get_unique_session_id_returns_evaluated_value(mock_page):
    mock_page.evaluate.return_value = asyncio.Future()
    mock_page.evaluate.return_value.set_result("mock-unique-session-id")

    unique_session_id = await pyppeteer.get_unique_session_id(mock_page)

    mock_page.assert_called
    assert unique_session_id == "mock-unique-session-id"


@pytest.mark.asyncio
async def test_get_page_returns_page():
    mock_page = asynctest.CoroutineMock()
    mock_page.return_value.set_result("test-page")
    mock_page.goto.return_value = asyncio.Future()
    mock_page.goto.return_value.set_result("should-not-be-seen")

    mock_browser = asynctest.CoroutineMock()
    mock_browser.newPage.return_value = asyncio.Future()
    mock_browser.newPage.return_value.set_result(mock_page)

    await pyppeteer.get_page(mock_browser)

    mock_browser.assert_called
    mock_page.goto.assert_called
