"""Test data."""

from faker import Faker

fake = Faker()


class Member:
    """Member Object."""

def __init__(self):
    self.first_name = fake.first_name()
    self.last_name = fake.last_name()
    self.email = fake.email()
    self.phone_number = fake.phone_number()
    self.date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%m-%d-%Y")
    self.birth_gender = fake.random.choice(["Male", "Female"])

@property
def full_name(self):
    """Return member full name."""
    return f"{self.first_name} {self.last_name}"
