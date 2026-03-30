"""Page object file for the provider sign-in page."""
from pages.provider_portal.provider_base_page import ProviderBasePage
from utils.env_config import EnvConfig


class ProviderSignInPage(ProviderBasePage):
    """Page object for the provider sign-in page."""
    URL = EnvConfig.PROVIDER_SIGN_IN_URL

    @property
    def email_input(self):
        """Email input on the provider sign-in page."""
        return self.page.get_by_role(role="textbox", name="email")

    @property
    def password_input(self):
        """Password input on the provider sign-in page."""
        return self.page.get_by_role(role="textbox", name="password")

    @property
    def submit_button(self):
        """Submit button on the provider sign-in page."""
        return self.page.get_by_role(role="button", name="submit")

    def login_with_email_and_password(self, email: str, password: str):
        """Sign in provider using email and password."""
        self.email_input.fill(f"{email}")
        self.password_input.fill(f"{password}")
        self.submit_button.click()
