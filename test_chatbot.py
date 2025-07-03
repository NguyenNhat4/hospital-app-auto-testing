import json
import os
import pytest
from playwright.sync_api import Page, expect

# --- Configuration ----------------------------------------------------------------
# Attempt to import the user's config.py. If it's not found, provide a helpful message.
try:
    import config
except ImportError:
    raise ImportError(
        "Could not import config.py. Please create this file by copying "
        "config.py.example and filling in your credentials."
    )

# --- Test Data --------------------------------------------------------------------
# Load test cases from the JSON file.
# This is a best practice called "data-driven testing".
with open("test_data.json", "r", encoding="utf-8") as f:
    test_data = json.load(f)

# --- Locators ---------------------------------------------------------------------
# Storing CSS selectors in one place makes them easier to update if the website's
# structure changes. This is a principle from the Page Object Model (POM) design pattern.
LOGIN_EMAIL_INPUT = "input[name='email']"
LOGIN_PASSWORD_INPUT = "input[name='pass']"
LOGIN_BUTTON = "button[name='login']"
PAGE_MESSAGE_BUTTON = "div[aria-label='Message']"
CHAT_INPUT_AREA = "div[aria-label='Message'][contenteditable='true']"
# This selector is crucial. It finds the last message in the chat that is NOT from the logged-in user.
# It looks for a message group that does not contain an element indicating it's "your message".
LAST_BOT_MESSAGE = "div[role='row']:last-of-type:not(:has(div[data-testid='outgoing_message'])) div[data-ad-preview='message']"
ACCEPT_COOKIES_BUTTON = "div[aria-label='Allow all cookies']"


# --- Pytest Fixtures --------------------------------------------------------------
# A fixture is a function that runs before a test. `pytest-playwright` provides the `page` fixture.
# We create our own fixture here to handle the login process efficiently.
@pytest.fixture(scope="session")
def page_with_login(browser):
    """
    A session-scoped fixture that handles logging into Facebook once and reuses
    the browser state for all tests in the session. This is much faster than
    logging in for every single test.
    """
    # Use a storage state file to cache login cookies and session information.
    # This file is added to .gitignore so it's not checked into version control.
    storage_state_file = "state.json"
    context = None
    page = None

    if os.path.exists(storage_state_file):
        # If the state file exists, reuse the existing authenticated context.
        context = browser.new_context(storage_state=storage_state_file)
        page = context.new_page()
        page.goto(config.FACEBOOK_PAGE_URL)
    else:
        # If no state file, perform a fresh login.
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.facebook.com")

        # Handle cookie consent dialog if it appears
        # We use a try-except block to gracefully handle the case where no cookie banner appears
        try:
            cookie_button = page.locator(ACCEPT_COOKIES_BUTTON).first
            cookie_button.click(timeout=5000)
        except Exception:
            # If the cookie button doesn't exist or times out, that's fine - just continue
            pass

        # Perform login
        page.locator(LOGIN_EMAIL_INPUT).fill(config.FACEBOOK_EMAIL)
        page.locator(LOGIN_PASSWORD_INPUT).fill(config.FACEBOOK_PASSWORD)
        page.locator(LOGIN_BUTTON).click()

        # Wait for navigation to complete after login, e.g., by waiting for a known element on the home page.
        # This is important to ensure the login was successful before proceeding.
        expect(page.locator("a[aria-label='Home']")).to_be_visible(timeout=30000)

        # Navigate to the target page and save the state
        page.goto(config.FACEBOOK_PAGE_URL)
        context.storage_state(path=storage_state_file)

    yield page

    # Teardown: close the context and browser after the test session is done.
    context.close()


# --- Test Cases -------------------------------------------------------------------
# This is the core of our testing.
# `@pytest.mark.parametrize` creates a version of the test for each item in `test_data`.
@pytest.mark.parametrize("test_case", test_data)
def test_chatbot_responses(page_with_login: Page, test_case: dict):
    """
    This single function tests all our chatbot cases from the JSON file.
    """
    page = page_with_login

    # 1. Open the chat window
    # We find the 'Message' button and click it to start a conversation.
    page.locator(PAGE_MESSAGE_BUTTON).click()

    # 2. Send a message to the bot
    # We find the chat input area, type our message, and press Enter.
    chat_input = page.locator(CHAT_INPUT_AREA)
    chat_input.type(test_case["message_to_send"])
    chat_input.press("Enter")

    # 3. Wait for and verify the bot's reply
    # We locate the last message from the bot and check if it contains our expected text.
    # `expect(locator).to_contain_text()` is a powerful Playwright assertion that automatically
    # waits for the element to appear and for its text to match.
    bot_reply_locator = page.locator(LAST_BOT_MESSAGE)

    expect(bot_reply_locator).to_contain_text(
        test_case["expected_reply"], timeout=15000  # Increased timeout for bot response
    ) 