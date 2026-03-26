"""Page object file for the booking page."""
from playwright.sync_api import Page
from pages.base_page import BasePage


class BookingPage(BasePage):
    """Page object for the booking page."""
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    @property
    def example_input(self):
        """Example input on the booking page."""
        return self.page.get_by_role("textbox", name="Example Input")

    @property
    def example_button(self):
        """Example button on the booking page."""
        return self.page.get_by_role("button", name="Example Button")

    def fill_booking_form(self, first_name: str, last_name: str):
        """Example method to fill out the booking form."""
        self.example_input.fill(f"{first_name} {last_name}")
        self.example_button.click()
