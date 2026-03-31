"""Member Registration Flow Tests"""

import pytest
from pages.member_portal.member_sign_in_page import MemberSignInPage
from pages.member_portal.member_join_page import MemberJoinPage
from pages.member_portal.registration.select_your_scan_page import SelectYourScanPage
from pages.member_portal.registration.schedule_your_scan import ScheduleYourScanPage
from pages.member_portal.registration.reserve_your_appointment import ReserveYourAppointmentPage
from pages.member_portal.registration.scan_confirm import ScanConfirmPage
from utils.test_data import Member, ScanProducts
import utils.stripe_helpers as stripe_helpers

@pytest.mark.member_registration
class TestMemberRegistration:
    """Tests for member registration flow."""

    def test_register_new_member(self, member_page):
        """Verify a new member can be registered successfully."""
        member = Member(scan_products=[ScanProducts.MRI_SCAN])

        sign_in_page = MemberSignInPage(member_page)
        sign_in_page.navigate()
        sign_in_page.join_button.click()

        join_page = MemberJoinPage(member_page)
        join_page.add_basic_member_info(member)

        select_scan_page = SelectYourScanPage(member_page)
        select_scan_page.select_your_scan(member)

        schedule_scan_page = ScheduleYourScanPage(member_page)
        schedule_scan_page.schedule_your_scan()

        reserve_your_appointment_page = ReserveYourAppointmentPage(member_page)
        reserve_your_appointment_page.add_credit_card(stripe_helpers.VALID_CARD_DETAILS,
                                                        member.postal_code)

        scan_confirm_page = ScanConfirmPage(member_page)
        confirmed_appointment_details = scan_confirm_page.get_confirmed_appointment()

        assert confirmed_appointment_details["scan_type"] == "MRI Scan"
        assert confirmed_appointment_details["location_name"] == "AMRIC"
        assert confirmed_appointment_details["location_address"] == "New York, city, NY 10022"
        assert confirmed_appointment_details["date"] == "Apr 16, 2026"
        assert confirmed_appointment_details["time"] == "10:30 AM EDT"

        scan_confirm_page.begin_medical_questionnaire_button.click()
