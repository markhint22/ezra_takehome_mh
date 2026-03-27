"""Page Object file for Select your scan page."""

from pages.base_page import BasePage
from utils.env_config import EnvConfig
from utils.test_data import Member


class SelectYourScanPage(BasePage):
    """Page Object for Select Your Scan Page."""
    URL = EnvConfig.MEMBER_SELECT_YOUR_SCAN_URL

    @property
    def date_of_birth_textbox(self):
        """Date of Birth Textbox."""
        return self.page.get_by_role(role='comboBox', name="date of birth")

    @property
    def gender_at_birth_select(self):
        """Gender at Birth Textbox"""
        return self.page.get_by_role(role="comboBox", name="sex at birth")

    def select_gender(self, gender: str):
        """Select gender"""
        self.gender_at_birth_select.click()
        self.page.get_by_Role(role="option", name=gender)

    def fill_select_your_scan_form(self, member: Member):
        """Fill select you scan form."""
        self.date_of_birth_textbox.fill(member.date_of_birth)
        self.select_gender(member.gender)
        #TODO: Select products to select, need method for this