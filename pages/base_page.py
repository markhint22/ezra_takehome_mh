"""Base page class for all page objects."""
from playwright.sync_api import Page


class BasePage:
    """Base page class for all page objects."""
    def __init__(self, page: Page):
        self.page = page

    def wait_for_page_load(self):
        """Wait for the page to fully load."""
        self.page.wait_for_load_state("networkidle")
