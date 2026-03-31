"""Page object page for Reserve Your Appointment Page."""

from playwright.sync_api import expect

from pages.member_portal.member_base_page import MemberBasePage
from utils.env_config import EnvConfig
from utils.stripe_helpers import CardDetails


class ReserveYourAppointmentPage(MemberBasePage):
    """Page Object for Reserve Your Appointment Page."""
    URL = EnvConfig.MEMBER_RESERVE_YOUR_APPOINTMENT_URL

    @property
    def card_payment_card(self):
        """Credit card payment card"""
        return self.page.locator("div.p-PaymentElement > div.p-PaymentAccordionButtonText",
                                has_text='card')

    @property
    def affirm_payment_card(self):
        """Affirm payment card"""
        return self.page.locator("div.p-PaymentElement > div.p-PaymentAccordionButtonText",
                                has_text='affirm')

    @property
    def bank_payment_card(self):
        """Bank payment card"""
        return self.page.locator("div.p-PaymentElement > div.p-PaymentAccordionButtonText",
                                has_text='bank')

    @property
    def back_button(self):
        """Back Button"""
        return self.page.get_by_role(role="button", name="back")

    @property
    def continue_button(self):
        """Continue Button"""
        return self.page.get_by_role(role="button", name='continue')


    #Card paypment card fields

    @property
    def payments_iframe(self):
        """Credit card iframe"""
        return self.page.frame_locator("iframe[title='Secure payment input frame']").first

    @property
    def credit_card_number_textbox(self):
        """Credit card number textbox"""
        return self.payments_iframe.locator("#payment-numberInput")

    @property
    def credit_card_expiration_date_textbox(self):
        """Credit card expiration date"""
        return self.payments_iframe.locator("#payment-expiryInput")

    @property
    def credit_card_security_code(self):
        """Credit card expiration date"""
        return self.payments_iframe.locator("#payment-cvcInput")

    @property
    def credit_card_country_combobox(self):
        """Credit card country comboBox"""
        return self.payments_iframe.locator("#payment-countryInput")

    @property
    def credit_card_postal_code_textbox(self):
        """Credit card postal code comboBox"""
        return self.payments_iframe.locator("#payment-postalCodeInput")

    def add_credit_card(self, card: CardDetails, postal_code: str):
        """Add the credit card."""
        expect(self.credit_card_number_textbox).to_be_visible()
        self.credit_card_number_textbox.fill(card.number)
        self.credit_card_expiration_date_textbox.fill(card.expiry)
        self.credit_card_security_code.fill(card.cvc)
        self.credit_card_postal_code_textbox.fill(postal_code)
        self.continue_button.click()
