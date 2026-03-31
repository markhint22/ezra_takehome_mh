"""Page Object page for Scan Confirm Page."""

import re

from playwright.sync_api import expect

from pages.member_portal.member_base_page import MemberBasePage
from utils.env_config import EnvConfig


class ScanConfirmPage(MemberBasePage):
    """Page Object for Scan Confirm Page."""
    URL = EnvConfig.MEMBER_SCAN_CONFIRM_URL

    @property
    def begin_medical_questionnaire_button(self):
        """Begin Medical Questionnaire button locator."""
        return self.page.get_by_role("button", name="begin medical questionnaire")


    # Appointment Details Locators

    @property
    def appointment_details(self):
        """Locator for the appointment details text."""
        return self.page.locator("div.scan-details")

    def _details_row(self, label: str):
        """Helper method to get a details row by its label."""
        return self.appointment_details.locator("div.scan-details__row").filter(
            has=self.page.locator("p", has_text=re.compile(
                rf"^\s*{re.escape(label)}\s*$", re.IGNORECASE),).first
        )

    @property
    def appointment_header(self):
        """Locator for the appointment header."""
        return self.appointment_details.locator("h4")

    @property
    def appointment_location_name(self):
        """Locator for the appointment location name."""
        return self._details_row("Location").locator("p").nth(1)

    @property
    def appointment_location_address(self):
        """Locator for the appointment location address."""
        return self._details_row("Location").locator("p").nth(2)

    @property
    def appointment_datetime(self):
        """Locator for the appointment date and time."""
        row = self._details_row("Date")
        return row.locator("p:has-text('Date') + p")

    def parse_scan_type(self, header_text: str):
        """Parse the scan type from the appointment header text."""
        return header_text.replace("Appointment","").strip()

    def parse_date_time_values(self, datetime_str: str):
        """Parse the date and time values from the appointment details."""
        date_str, separator, time_str_with_timezone = datetime_str.partition("\u2022")
        if not separator:
            raise ValueError(f"Unexpected date/time format: '{datetime_str}'")
        time_str, time_zone_str = time_str_with_timezone.rsplit(" ", 1)
        return date_str.strip(), time_str.strip(), time_zone_str.strip()

    def get_confirmed_appointment(self):
        """Get the appointment details for assertions."""
        expect(self.appointment_header).to_be_visible(timeout=10000)

        date_parsed, time_parsed, time_zone_parsed = self.parse_date_time_values(
            self.appointment_datetime.text_content())
        return {
            "scan_type": self.parse_scan_type(self.appointment_header.text_content()),
            "location_name": self.appointment_location_name.text_content(),
            "location_address": self.appointment_location_address.text_content(),
            "date": date_parsed,
            "time": time_parsed,
            "time_zone": time_zone_parsed
        }
