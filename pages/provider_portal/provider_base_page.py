"""Base page class for provider portal pages."""
from pages.base_page import BasePage


class ProviderBasePage(BasePage):
    """Base page for all provider portal page objects."""

    def dismiss_cookies_banner(self):
        """Dismiss cookies consent banner if present."""
        accept_button = self.page.get_by_role(role="button", name="i understand")
        if accept_button.is_visible():
            accept_button.click()

    def navigate(self):
        """Override base page navigate to include dismiss cookies banner on provider portal pages."""
        super().navigate()
        self.dismiss_cookies_banner()
