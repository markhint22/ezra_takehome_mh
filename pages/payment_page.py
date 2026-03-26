"""Page object file for the payment page."""
from pages.base_page import BasePage


class PaymentPage(BasePage):
    """Page object for the payment page."""
    def __init__(self, page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    @property
    def example_input(self):
        """Example input on the payment page."""
        return self.page.get_by_role("textbox", name="Example Input")

    @property
    def example_button(self):
        """Example button on the payment page."""
        return self.page.get_by_role("button", name="Example Button")

    def fill_payment_form(self, first_name: str, last_name: str):
        """Example method to fill out the payment form."""
        self.example_input.fill(f"{first_name} {last_name}")
        self.example_button.click()
