"""Root conftest.py for pytest."""
from pathlib import Path

import pytest
from playwright.sync_api import Browser

from utils.env_config import EnvConfig
from pages.provider_portal.provider_sign_in_page import ProviderSignInPage

AUTH_STATE_DIR = Path(__file__).parent / ".auth"
PROVIDER_AUTH_STATE = AUTH_STATE_DIR / "provider_state.json"


@pytest.fixture(scope='session')
def provider_auth_state(browser: Browser) -> Path:
    """Log in to Provider once per session, save storageSpace for reuse."""
    AUTH_STATE_DIR.mkdir(exist_ok=True)

    context = browser.new_context()
    page = context.new_page()

    sign_in_page = ProviderSignInPage(page)
    sign_in_page.navigate()
    sign_in_page.login_with_email_and_password(
        email=EnvConfig.PROVIDER_USERNAME,
        password=EnvConfig.PROVIDER_PASSWORD
        )
