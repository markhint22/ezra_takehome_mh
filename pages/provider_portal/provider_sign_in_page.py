"""Page object file for the booking page."""
from pages.base_page import BasePage
from utils.env_config import EnvConfig


class ProviderSignInPage(BasePage):
    """Page object for the provider sign-in page."""
    URL = EnvConfig.PROVIDER_SIGN_IN_URL

    def navigate(self):
        """Navigate to this page."""
        self.page.goto(self.URL)
        self.wait_for_page_load()

    @property
    def email_input(self):
        """Email input on the provider sign-in page."""
        return self.page.get_by_role("input", id="email")

    @property
    def password_input(self):
        """Password input on the provider sign-in page."""
        return self.page.get_by_role("input", id="password")

    @property
    def submit_button(self):
        """Submit button on the provider sign-in page."""
        return self.page.locator("button.submit-btn")

    def login_with_email_and_password(self, email: str, password: str):
        """Sign in provider using email and password."""
        self.email_input.fill(f"{email}")
        self.password_input.fill(f"{password}")
        self.submit_button.click()
