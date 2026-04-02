# Ezra Take-Home Submission

End-to-end UI automation suite for member and provider workflows using Playwright + Pytest with a Page Object Model architecture.

## Installation Instructions

1. Install Poetry:
   https://python-poetry.org/docs/

2. Configure Poetry to create the virtual environment inside the repo:
   poetry config virtualenvs.in-project true

3. Install dependencies:
   poetry install

4. Install Playwright browsers:
   poetry run playwright install chromium

5. Configure environment variables:
   cp .env.example .env

6. Update .env with valid staging credentials and URLs before running tests.

## Running Tests

Run all tests:
poetry run pytest

Run registration tests only:
poetry run pytest tests/registration -v

Run a single registration test:
poetry run pytest tests/registration/test_registration.py::TestMemberRegistration::test_register_new_member -v

Run with visible browser:
poetry run pytest --headed

Notes:
- Tests are configured via [pyproject.toml](pyproject.toml) and [conftest.py](conftest.py)
- The suite expects valid .env values for provider/member environments

## Project Structure

[conftest.py](conftest.py)
- Shared Pytest fixtures and browser context setup

pages/
- Page Object classes for UI interactions
- member_portal/: member registration and scheduling flows
- provider_portal/: provider sign-in and provider workflows

tests/
- Automated test suites grouped by area
- registration/: member registration coverage

utils/
- [env_config.py](utils/env_config.py): environment/config loading
- [test_data.py](utils/test_data.py): generated test users and scan selections
- [stripe_helpers.py](utils/stripe_helpers.py): Stripe test card inputs and helpers

[pyproject.toml](pyproject.toml)
- Dependency management and Pytest configuration

## Design Decisions

- Page Object Model:
  UI actions and locators are encapsulated in page classes to keep tests readable and maintainable.

- Pytest + Playwright:
  Pytest provides fixtures and test organization; Playwright provides stable browser automation and assertions.

- Environment Variables:
  Sensitive values are stored in .env and excluded from source control.

- Realistic Registration Coverage:
  Current registration tests include:
  - Successful member registration flow
  - Declined card negative path
  - Required-field validation behavior

- Deterministic Test Data:
  Test user data is generated through test_data.py to reduce collisions and improve repeatability.

## Assumptions

- Tests run against Ezra staging environments.
- Required credentials and base URLs are available in .env.
- Network access is available from the test machine to the target environments.