"""Member Registration Flow Tests"""

import pytest
from pages.member_portal.member_sign_in_page import MemberSignInPage
from pages.member_portal.member_join_page import MemberJoinPage
from pages.member_portal.registration.select_your_scan_page import SelectYourScanPage
from utils.test_data import Member, ScanProducts

@pytest.mark.member_registration
class TestMemberRegistration:
    """Tests for member registration flow."""

    def test_register_new_member(self, member_page):
        """Verify a new member can be registered successfully."""
        member = Member([ScanProducts.HEART_SCAN])
        sign_in_page = MemberSignInPage(member_page)
        sign_in_page.navigate()
        sign_in_page.join_button.click()
        sign_in_page.wait_for_page_load()

        join_page = MemberJoinPage(member_page)
        join_page.fill_join_form(member)
        join_page.wait_for_page_load()

        scan_page = SelectYourScanPage(member_page)
        scan_page.fill_select_your_scan_form(member)
        scan_page.wait_for_page_load()
