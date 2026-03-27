"""Member Registration Flow Tests"""

import pytest
from pages.member_portal.member_sign_in_page import MemberSignInPage
from pages.member_portal.member_join_page import MemberJoinPage
from utils.test_data import Member

@pytest.mark.member_registration
class TestMemberRegistration:
    """Tests for member registration flow."""

    def test_register_new_member(self, member_page):
        """Verify a new member can be registered successfully."""
        member = Member()
        sign_in_page = MemberSignInPage(member_page)
        sign_in_page.join_button.click()
        sign_in_page.wait_for_page_load()

        join_page = MemberJoinPage(member_page)
        join_page.fill_join_form(member)
