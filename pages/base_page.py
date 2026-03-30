"""Base page class for all page objects."""
from playwright.sync_api import Page


class BasePage:
    """Base page class for all page objects."""
    URL = ""

    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        """Navigate directly to this page."""
        self.page.goto(self.URL)
        self.wait_for_page_load()

    def wait_for_page_load(self):
        """Wait for the page to fully load."""
        self.page.wait_for_load_state("domcontentloaded")

    def wait_for_this_page_url(self):
        """Wait for the URL to match this page's URL."""
        self.page.wait_for_url(f"{self.URL}**")
