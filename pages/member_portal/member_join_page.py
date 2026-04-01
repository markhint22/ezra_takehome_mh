"""Page object for the member join page."""

from pages.member_portal.member_base_page import MemberBasePage
from utils.env_config import EnvConfig
from utils.test_data import Member


class MemberJoinPage(MemberBasePage):
    """Page object for the member join page."""
    URL = EnvConfig.MEMBER_JOIN_URL

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
        return self.page.get_by_role(role="textbox", name="password")

    @property
    def terms_of_use_checkbox(self):
        """Terms of Use Checkbox"""
        return self.page.get_by_role(role="button", name="I agree to Ezra's terms of use")

    @property
    def marketing_emails_checkbox(self):
        """Marketing Emails Agreement Checkbox"""
        return self.page.get_by_role(role="button",
                                    name="I agree to receive marketing communications via email")

    @property
    def marketing_sms_checkbox(self):
        """Marketing SMS Agreement Checkbox"""
        return self.page.get_by_role(role="button",
                                    name="marketing messages via telephone and sms")

    @property
    def submit_button(self):
        """Submit button"""
        return self.page.get_by_role(role="button", name="submit")

    @property
    def last_name_missing_error_message(self):
        """Last Name Missing Error Message"""
        return self.page.locator("p", has_text="The Legal Last Name field is required.")

    def add_basic_member_info(self, member: Member):
        """Add basic member information."""
        self.wait_for_this_page_url()
        self.first_name_textbox.fill(member.first_name)
        self.last_name_textbox.fill(member.last_name)
        self.email_textbox.fill(member.email)
        self.phone_number_textbox.fill(member.phone_number)
        self.password_textbox.fill(member.password)
        self.terms_of_use_checkbox.click()
        self.marketing_emails_checkbox.click()
        self.marketing_sms_checkbox.click()
        self.page.wait_for_timeout(1000)
        # Wait for any potential async validation to complete before clicking submit
        self.wait_for_page_load()
        self.submit_button.click()
