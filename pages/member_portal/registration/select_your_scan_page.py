"""Page Object file for Select your scan page."""

import re

from pages.member_portal.member_base_page import MemberBasePage
from utils.env_config import EnvConfig
from utils.test_data import Member


class SelectYourScanPage(MemberBasePage):
    """Page Object for Select Your Scan Page."""
    URL = EnvConfig.MEMBER_SELECT_YOUR_SCAN_URL

    @property
    def date_of_birth_textbox(self):
        """Date of Birth Textbox."""
        return self.page.get_by_role(role='textBox', name="date of birth")

    @property
    def gender_combobox(self):
        """Gender at Birth Textbox"""
        return self.page.locator(
            ".container--inner",
            has=self.page.get_by_text("What was your sex at birth")
        ).locator(".multiselect")

    @property
    def cancel_button(self):
        """Cancel Button"""
        return self.page.get_by_role(role="button", name="cancel")

    @property
    def continue_button(self):
        """Continue Button"""
        return self.page.get_by_role(role="button", name="continue")

    def select_gender(self, gender: str):
        """Select gender at birth."""
        self.gender_combobox.wait_for(state="visible")
        self.gender_combobox.click()
        self.page.get_by_role(role="option", name=gender).filter(
            has_text=re.compile(f"^{gender}$", re.IGNORECASE)).click()

    def select_scan_products(self, product_names: list[str]):
        """Select products to scan."""
        for name in product_names:
            card = self.page.locator(".encounter-card").filter(has=self.page
            .locator("p.encounter-title", has_text=re.compile(f"^{name}$", re.IGNORECASE)))
            card.click()

    def select_your_scan(self, member: Member):
        """Select your scan."""
        self.wait_for_this_page_url()
        self.date_of_birth_textbox.fill(member.date_of_birth.replace("-",""))
        self.select_gender(member.gender)
        self.select_scan_products(member.scan_products)
        self.continue_button.click()
