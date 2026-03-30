"""Base page class for member portal pages."""
from pages.base_page import BasePage


class MemberBasePage(BasePage):
    """Base page for all member portal page objects."""

    def dismiss_cookies_banner(self):
        """Dismiss cookies consent banner if present."""
        accept_button = self.page.get_by_role(role="button", name="accept")
        if accept_button.is_visible():
            accept_button.click()

    def navigate(self):
        """Override base page navigate to include dismiss cookies banner on member portal pages."""
        super().navigate()
        self.dismiss_cookies_banner()
