"""Member Registration Flow Tests"""

import re
import pytest
from playwright.sync_api import expect

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
        member = Member(scan_product=ScanProducts.MRI_SCAN)

        sign_in_page = MemberSignInPage(member_page)
        sign_in_page.navigate()
        sign_in_page.join_button.click()

        join_page = MemberJoinPage(member_page)
        join_page.add_basic_member_info(member)

        select_scan_page = SelectYourScanPage(member_page)
        selected_scan_type = select_scan_page.select_your_scan(member)["selected_scan_type"]

        schedule_scan_page = ScheduleYourScanPage(member_page)
        selected_schedule_details = schedule_scan_page.schedule_your_scan()

        reserve_your_appointment_page = ReserveYourAppointmentPage(member_page)
        reserve_your_appointment_page.add_credit_card(
            stripe_helpers.VALID_CARD_DETAILS,
            member.postal_code, member.email, member.phone_number)

        scan_confirm_page = ScanConfirmPage(member_page)
        confirmed_appointment_details = scan_confirm_page.get_confirmed_appointment()

        assert confirmed_appointment_details["confirmed_scan_type"] == selected_scan_type
        assert confirmed_appointment_details[
            "confirmed_location_name"] == selected_schedule_details["selected_location_name"]
        assert confirmed_appointment_details[
            "confirmed_location_address"].replace("  ", " ") == selected_schedule_details[
            "selected_location_address"].replace("  ", " ")
        assert confirmed_appointment_details[
            "confirmed_datetime"] == selected_schedule_details["selected_datetime"]
        assert confirmed_appointment_details["confirmed_time_zone"] in ["EDT", "EST"]

    def test_register_new_member_declined_credit_card_blocks_registration(self, member_page):
        """Verify that a declined credit card blocks registration."""
        member = Member(scan_product=ScanProducts.LUNGS_CT_SCAN)

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
        reserve_your_appointment_page.add_credit_card(
            stripe_helpers.DECLINED_CARD_DETAILS,
            member.postal_code, member.email, member.phone_number)

        expect(reserve_your_appointment_page.declined_card_error_message).to_be_visible(
            timeout=10000)
        expect(reserve_your_appointment_page.declined_payment_error_message).to_be_visible(
            timeout=10000)

    def test_register_new_member_required_fields_not_provided(self, member_page):
        """Verify that a new member cannot be registered if required fields are not provided."""
        member = Member(scan_product=ScanProducts.MRI_SCAN)
        member.last_name = ""

        sign_in_page = MemberSignInPage(member_page)
        sign_in_page.navigate()
        sign_in_page.join_button.click()

        join_page = MemberJoinPage(member_page)
        join_page.add_basic_member_info(member)
        expect(join_page.last_name_missing_error_message).to_be_visible(timeout=10000)
        expect(join_page.submit_button).to_have_class(
            re.compile(r".+--appear-disabled-new"), timeout=10000)
