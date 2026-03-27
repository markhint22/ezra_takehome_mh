"""Page object for the member join page."""

from pages.base_page import BasePage
from utils.env_config import EnvConfig
from utils.test_data import Member


class MemberJoinPage(BasePage):
    """Page object for the member join page."""
    URL = EnvConfig.MEMBER_JOIN_URL

    def navigate(self):
        """Navigate directly to this page."""
        self.page.goto(self.URL)
        self.wait_for_page_load()

    @property
    def google_sign_up_button(self):
        """Sign Up with Google Button"""
        return self.page.get_by_label("sign up with google")

    @property
    def first_name_textbox(self):
        """First Name Textbox"""
        return self.page.get_by_role(role="textbox", name="legal first name")

    @property
    def last_name_textbox(self):
        """Last Name Textbox"""
        return self.page.get_by_role(role="textbox", name="legal last name")

    @property
    def email_textbox(self):
        """Email Textbox"""
        return self.page.get_by_role(role="textbox", name="email")

    @property
    def phone_number_textbox(self):
        """Phone Number Textbox"""
        return self.page.get_by_role(role="textbox", name="phone number")

    @property
    def password_textbox(self):
        """Password Textbox"""
        return self.page.get_by_label("password")

    @property
    def terms_of_use_checkbox(self):
        """Terms of Use Checkbox"""
        return self.page.get_by_role(role="button", name="terms of use")

    @property
    def marketing_emails_checkbox(self):
        """Marketing Emails Agreement Checkbox"""
        return self.page.get_by_role(role="button", name="marketing communications via email")

    @property
    def markething_sms_checkbox(self):
        """Marketing SMS Agreement Checkbox"""
        return self.page.get_by_role(role="button", name="marketing messages via telephone and sms")

    @property
    def submit_button(self):
        """Submit button"""
        return self.page.get_by_role(role="button", name="submit")

    def fill_join_form(self, member: Member):
        """Fill the new member join form."""
        self.first_name_textbox.fill(member.first_name)
        self.last_name_textbox.fill(member.last_name)
        self.email_textbox.fill(member.email)
        self.phone_number_textbox.fill(member.phone_number)
        self.password_textbox.fill(member.password)
        self.terms_of_use_checkbox.click()
        self.marketing_emails_checkbox.click()
        self.markething_sms_checkbox.click()
        self.wait_for_page_load()