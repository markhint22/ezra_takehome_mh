"""Page object file for the member sign-in page."""
from pages.base_page import BasePage
from utils.env_config import EnvConfig


class MemberSignInPage(BasePage):
    """Page object for the member sign-in page."""
    URL = EnvConfig.MEMBER_SIGN_IN_URL

    def navigate(self):
        """Navigate to this page."""
        self.page.goto(self.URL)
        self.wait_for_page_load()

    @property
    def join_button(self):
        """Join button on the member sign-in page."""
        return self.page.get_by_role(role="link", name="join")

    @property
    def email_input(self):
        """Email input on the member sign-in page."""
        return self.page.get_by_role(role="textbox", name="email")

    @property
    def password_input(self):
        """Password input on the member sign-in page."""
        return self.page.get_by_role(role="textbox", name="password")

    @property
    def submit_button(self):
        """Submit button on the member sign-in page."""
        return self.page.get_by_role(role="button", name="submit")

    def login_with_email_and_password(self, email: str, password: str):
        """Sign in member using email and password."""
        self.email_input.fill(f"{email}")
        self.password_input.fill(f"{password}")
        self.submit_button.click()
