"""Page Object file for Schedule Your Scan page."""

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

    def select_first_scan_location_card(self):
        """Select first scan location card."""
        return self.page.locator(".location-card").first.click()

    def select_state(self, state: str):
        """Select state from member state value."""
        self.state_combobox.wait_for(state="visible")
        self.state_combobox.click()
        self.page.get_by_role(role="option", name=state).filter(has_text=state).click()

    def select_first_active_date(self, max_months: int = 12):
        """Click the first active date in the calendar"""
        calendar = self.page.locator("div.datepicker")
        next_month_button = self.page.locator("div.arrows").locator("button.header-btn").nth(1)

        for _ in range(max_months):
            active_dates = calendar.locator("div:has(>span[aria-disabled='false'])")
            if active_dates.count() > 0:
                first_active_date = active_dates.first
                first_active_date.wait_for(state="visible")
                first_active_date.click()
                return

            next_month_button.click()
            calendar.wait_for(state="visible")

        raise AssertionError("No active scan dates found for user.")

    def select_first_available_time_slot(self):
        """Click the first available time slot available on the selected day."""
        return self.page.locator("div.appointments__individual-appointment").first.click()

    def fill_schedule_your_scan_form(self):
        """Fill the schedule your scan form."""
        self.wait_for_this_page_url()
        self.find_closest_centers_to_me_button.click()
        self.wait_for_page_load()
        self.select_first_active_date()
        self.select_first_available_time_slot()
        self.continue_button.wait_for(state="active")
        self.continue_button.click()
