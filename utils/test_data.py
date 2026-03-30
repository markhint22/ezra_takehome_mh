"""Test data."""

import random
from faker import Faker

fake = Faker()

DEFAULT_PASSWORD = "Test132435!"

class ScanProducts:
    """Products Object."""
    MRI_SCAN = "MRI Scan"
    MRI_SCAN_WITH_SPINE = "MRI Scan with Spine"
    MRI_SCAN_WITH_SKELETAL_AND_NEUROLOGICAL_ASSESSMENT = "MRI Scan with Skeletal and Neurological Assessment"
    HEART_SCAN = "Heart CT Scan"
    LUNGS_CT_SCAN = "Lungs CT Scan"


class Member:
    """Member Object."""

    def __init__(self, scan_products=None):
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.email = fake.email()
        self.password = DEFAULT_PASSWORD
        self.phone_number = fake.phone_number()
        self.date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%m-%d-%Y")
        self.birth_gender = random.choice(["Male", "Female"])
        self.scan_products = scan_products if scan_products else []

    @property
    def full_name(self):
        """Return member full name."""
        return f"{self.first_name} {self.last_name}"
