"""Root conftest.py for pytest."""

from pathlib import Path

import pytest
from playwright.sync_api import Browser

from utils.env_config import EnvConfig
from pages.provider_portal.provider_sign_in_page import ProviderSignInPage

AUTH_STATE_DIR = Path(__file__).parent / ".auth"
PROVIDER_AUTH_STATE = AUTH_STATE_DIR / "provider_state.json"
BROWSER_CONTEXT_ARGS = {"permissions": ["notifications", "geolocation"],
                        "geolocation": {"latitude": 40.7128, "longitude": -74.0060}
                        } # New York City geolocation


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args): # pylint: disable=redefined-outer-name
    """Use environment-driven Playwright launch options."""
    return {
        **browser_type_launch_args,
        "headless": EnvConfig.HEADLESS,
        "slow_mo": EnvConfig.SLOW_MO,
    }


@pytest.fixture(scope='session')
def provider_auth_state(browser: Browser) -> Path:
    """Log in to Provider once per session, save storageSpace for reuse."""
    AUTH_STATE_DIR.mkdir(exist_ok=True)

    context = browser.new_context(**BROWSER_CONTEXT_ARGS)
    page = context.new_page()

    sign_in_page = ProviderSignInPage(page)
    sign_in_page.navigate()
    sign_in_page.login_with_email_and_password(
        email=EnvConfig.PROVIDER_USERNAME,
        password=EnvConfig.PROVIDER_PASSWORD
        )
    page.wait_for_url(f"{EnvConfig.PROVIDER_BASE_URL}/**", timeout=15000)

    context.storage_state(path=str(PROVIDER_AUTH_STATE))
    context.close()
    return PROVIDER_AUTH_STATE

@pytest.fixture()
def provider_page(browser: Browser, provider_auth_state: Path): # pylint: disable=redefined-outer-name
    """Provide a fresh page with auth state loaded for each test."""
    context = browser.new_context(storage_state=str(provider_auth_state), **BROWSER_CONTEXT_ARGS)
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture()
def member_page(browser: Browser):
    """Provide a fresh unauthenticated member page."""
    context = browser.new_context(**BROWSER_CONTEXT_ARGS)
    page = context.new_page()
    yield page
    context.close()
