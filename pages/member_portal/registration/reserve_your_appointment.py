"""Page object page for Reserve Your Appointment Page."""

from  pages.member_portal.member_base_page import MemberBasePage
from utils.env_config import EnvConfig

class ReserveYourAppointmentPage(MemberBasePage):
    """Page Object for Reserve Your Appointment Page."""
    URL = EnvConfig.MEMBER_RESERVE_YOUR_APPOINTMENT_URL

    @property
    def card_payment_card(self):
        """Credit card payment card"""
        return self.page.locator("div.p-PaymentElement > div.p-PaymentAccordionButtonText", has_text='card')

    @property
    def affirm_payment_card(self):
        """Affirm payment card"""
        return self.page.locator("div.p-PaymentElement > div.p-PaymentAccordionButtonText", has_text='affirm')

    @property
    def bank_payment_card(self):
        """Bank payment card"""
        return self.page.locator("div.p-PaymentElement > div.p-PaymentAccordionButtonText", has_text='bank')

    @property
    def back_button(self):
        """Back Button"""
        return self.page.get_by_role(role="button", name="back")

    @property
    def continue_button(self):
        """Continue Button"""
        return self.page.get_by_role(role="button", name='continue')