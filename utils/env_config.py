"""Environment configuration."""
import os


class EnvConfig:
    """Centralized configuration loaded from .env file."""

    # Member Portal URLs
    MEMBER_BASE_URL = os.getenv("MEMBER_BASE_URL", "https://myezra-staging.ezra.com").rstrip("/")
    MEMBER_SIGN_IN_URL = os.getenv("MEMBER_SIGN_IN_URL", f"{MEMBER_BASE_URL}/signin")
    MEMBER_JOIN_URL = os.getenv("MEMBER_JOIN_URL", f"{MEMBER_BASE_URL}/join")
    MEMBER_SELECT_YOUR_SCAN_URL = os.getenv("MEMBER_SELECT_YOUR_SCAN_URL", f"{MEMBER_BASE_URL}/sign-up/select-plan")
    MEMBER_SCHEDULE_YOUR_SCAN_URL = os.getenv("MEMBER_SCHEDULE_YOUR_SCAN_URL", f"{MEMBER_BASE_URL}/sign-up/schedule-scan")
    MEMBER_RESERVE_YOUR_APPOINTMENT_URL = os.getenv("MEMBER_RESERVE_YOUR_APPOINTMENT_URL", f"{MEMBER_BASE_URL}/sign-up/reserve-appointment")

    # Provier Portal URLs
    PROVIDER_BASE_URL = os.getenv("PROVIDER_BASE_URL", "https://staging-hub.ezra.com").rstrip("/")
    PROVIDER_SIGN_IN_URL = os.getenv("PROVIDER_SIGN_IN_URL", f"{PROVIDER_BASE_URL}/signin")

    # Provider credentials
    PROVIDER_USERNAME = os.getenv("PROVIDER_USERNAME","")
    PROVIDER_PASSWORD = os.getenv("PROVIDER_PASSWORD","")

    # Browser settings
    HEADLESS = os.getenv("HEADLESS", "true").lower() != "false"
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))
