"""Page Object file for Schedule Your Scan page."""

from datetime import datetime

from playwright.sync_api import expect

from pages.member_portal.member_base_page import MemberBasePage
from utils.env_config import EnvConfig

class ScheduleYourScanPage(MemberBasePage):
    """Page object for Schedule Your Scan Page."""
    URL = EnvConfig.MEMBER_SCHEDULE_YOUR_SCAN_URL


    @property
    def state_combobox(self):
        """State ComboBox"""
        return self.page.get_by_role(role="combobox", name="state")

    @property
    def find_closest_centers_to_me_button(self):
        """Find closest centers to me button"""
        return self.page.get_by_role(role="button", name="find closest centers to me")

    @property
    def continue_button(self):
        """Continue Button"""
        return self.page.get_by_role(role="button", name="continue")

    @property
    def calendar(self):
        """Calendar widget for selecting scan date."""
        return self.page.locator("div.datepicker")

    @property
    def time_slots(self):
        """Time slots for scan appointments."""
        return self.page.locator("div.appointments__individual-appointment")

    @property
    def location_cards(self):
        """Scan location cards."""
        return self.page.locator(".location-card")

    def select_first_scan_location_card(self):
        """Select first scan location card."""
        expect(self.location_cards.first).to_be_visible(timeout=5000)
        self.page.wait_for_timeout(1000)  # Wait for potential animations to complete
        first_card = self.location_cards.first

        location_name = first_card.locator("p").nth(0).text_content().strip()
        location_address = first_card.locator("p").nth(2).text_content().strip()

        first_card.click()
        return {"selected_location_name": location_name, "selected_location_address": location_address}

    def select_state(self, state: str):
        """Select state from member state value."""
        expect(self.state_combobox).to_be_enabled(timeout=5000)
        self.state_combobox.click()
        self.page.get_by_role(role="option", name=state).filter(has_text=state).click()

    def select_first_active_date(self, max_months: int = 12):
        """Click the first active date in the calendar"""
        expect(self.calendar).to_be_visible(timeout=30000)
        self.page.wait_for_timeout(5000)  # Wait for potential animations to complete
        next_month_button = self.page.locator("div.arrows").locator("button.header-btn").nth(1)

        for _ in range(max_months):
            active_dates = self.calendar.locator(".vuecal__cell:not(.vuecal__cell--disabled):not(.vuecal__cell--out-of-scope)")
            if active_dates.count() > 0:
                first_active_date = active_dates.first
                expect(first_active_date).to_be_enabled(timeout=5000)
                self.page.wait_for_timeout(5000)  # Wait for potential animations to complete


                calendar_header = self.calendar.locator("div.calendar-title").locator("button.trigger-btn").locator("p").text_content().strip()
                day_text = first_active_date.locator("span.vc-day-content").locator("div").nth(1).text_content().strip()
                formatted_date = f"{calendar_header.rsplit(' ', 1)[0]} {day_text}, {calendar_header.rsplit(' ', 1)[1]}"

                first_active_date.click()
                return formatted_date

            next_month_button.click()
            expect(self.calendar).to_be_enabled(timeout=5000)

        raise AssertionError("No active scan dates found for user.")

    def select_first_available_time_slot(self):
        """Click the first available time slot available on the selected day."""
        first_time_slot = self.time_slots.first
        expect(first_time_slot).to_be_visible(timeout=10000)
        time_text = first_time_slot.locator("div").text_content().strip()

        first_time_slot.click()
        return {"selected_time": time_text.strip()}

    def schedule_your_scan(self) -> dict:
        """Schedule your scan."""
        self.wait_for_this_page_url()
        self.find_closest_centers_to_me_button.click()
        location_details = self.select_first_scan_location_card()
        selected_date = self.select_first_active_date()
        selected_time = self.select_first_available_time_slot()

        combined = f"{selected_date} {selected_time['selected_time']}"
        selected_datetime = None
        for fmt in ("%b %d, %Y %I:%M %p", "%B %d, %Y %I:%M %p",
                    "%b %d, %Y %H:%M", "%B %d, %Y %H:%M"):
            try:
                selected_datetime = datetime.strptime(combined, fmt)
                break
            except ValueError:
                continue

        if selected_datetime is None:
            raise ValueError(f"Could not parse: {combined!r}")

        expect(self.continue_button).to_be_enabled(timeout=5000)
        self.continue_button.click()

        return {
            **location_details,
            "selected_datetime": selected_datetime
        }
