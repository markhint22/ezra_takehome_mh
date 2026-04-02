# Ezra Take-Home Submission

End-to-end UI automation suite for member and provider workflows using Playwright + Pytest with a Page Object Model architecture.

## Installation Instructions

1. Install Poetry:
   [See the Poetry documentation](https://python-poetry.org/docs/)

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
set `HEADLESS=false` in `.env`, then run:
poetry run pytest

Notes:

- Tests are configured via [pyproject.toml](pyproject.toml) and [conftest.py](conftest.py)
- The suite expects valid .env values for provider/member environments
- Browser mode is environment-driven via [env_config.py](utils/env_config.py): `HEADLESS=false` for local headed runs, `HEADLESS=true` for CI/headless runs.

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

- Env Config Boundary:
  Environment-specific URLs and configuration are referenced through page objects and centralized via [env_config.py](utils/env_config.py), which keeps tests environment-agnostic and reduces hardcoded endpoint usage in test files.

- Assertion Strategy:
  Business outcome assertions are kept at the test layer (test face) for clear test intent and reporting, while `expect(...)` calls in page objects are used for flow synchronization and UI actionability checks (for example visibility/enabled state before interactions).

- Object Ownership and Atomic Methods:
  Domain/test objects are kept in the test layer as much as possible, while page objects remain focused on atomic UI actions. This keeps page methods small, composable, and reusable across multiple test scenarios without embedding test-specific state.

- Realistic Registration Coverage:
  Current registration tests include:
  - Successful member registration flow
  - Declined card negative path
  - Required-field validation behavior

- Deterministic Test Data:
  Test user data is generated through test_data.py to reduce collisions and improve repeatability.
  For Stripe compatibility, phone area code is currently hardcoded to a known valid value for simplicity and deterministic reliability.

## Assumptions

- Tests run against Ezra staging environments.
- Required credentials and base URLs are available in .env.
- Network access is available from the test machine to the target environments.

## Take-Home Test Answers

## Automation Approach

### Why These 3 Tests Were Chosen for Automation

1. **Happy-path registration (test_register_new_member):**
Core revenue-critical workflow; highest business impact if broken.
Exercises end-to-end system integration: identity → scan selection → scheduling → payment → confirmation.
Provides fastest feedback on regressions in the primary user journey.

1. **Declined card blocking (test_register_new_member_declined_credit_card_blocks_registration):**
Validates payment failure handling, a critical security and financial boundary.
Requires minimal setup but tests a distinct failure mode distinct from happy path.
Lower flakiness than complex error handling tests (payment processing is deterministic with Stripe test cards).

1. **Required-field validation (test_register_new_member_required_fields_not_provided):**
Fast, isolated, and UI-focused; does not require backend services or payment processing.
Catches regressions in client-side form validation early in the pipeline.
Provides rapid feedback without external dependencies.

### Trade-Offs

**Development Velocity vs Exhaustive Coverage:**

- Trade-off: Automating all 15 tests would require significant time investment upfront and ongoing maintenance overhead.
- Decision: Focused on P0 tests (3 tests) to deliver measurable value quickly, with a roadmap to expand coverage iteratively.

**Deterministic Test Data:**

- Trade-off: Generated test data (via Faker) reduces collisions but can hide environment-specific bugs.
- Decision: Use generated data for flexibility and isolation; supplement with seed-based data for environment-specific edge cases if needed.

**Playwright Headed Mode:**

- Trade-off: Running tests in headed mode improves demo/review visibility but increases execution time and resource usage.
- Decision: Browser mode is controlled by `.env`/environment variables through `EnvConfig.HEADLESS`; use `HEADLESS=false` locally so reviewers can watch the flow, and `HEADLESS=true` in CI for speed and stability.
- CI Assumption: The pipeline sets `HEADLESS=true` (or equivalent environment override) during CI execution.

### Scalability Considerations

**Parallel Execution:**

- Current setup: Tests run sequentially in the default configuration.
- Recommendation: Enable pytest-xdist with `pytest -n auto` for parallel execution, but requires context isolation to avoid state collisions. pytest-xdist is not added to dependencies yet so this is not currently enabled.
- Caveat: Stripe test card interactions and appointment slot contention may require test ordering or per-test fixtures.

**Flakiness and Resilience:**

- Main sources: Network delays, date/time boundaries (calendar availability), Stripe API latency.
- Mitigations implemented: Implicit waits were used as much as possible. Explicit `expect(...).to_be_visible(timeout=10000)` waits used instead of hardcoded sleeps; context setup in conftest.
- Future: Implement retry-on-flakiness via pytest-rerunfailures with smarter failure detection. Remove remaining explicit waits.

**Test Data Lifecycle:**

- Current: Generated data is ephemeral per test run.
- Future: Implement test data seeding (deterministic Faker seeds) for reproducibility and cleanup helpers for test isolation.

**Environment-Specific Hardcoding:**

- Current: Geolocation (NYC) and timezone (EDT/EST) are hardcoded in conftest.
- Future: Parametrize locale/timezone tests and validate behavior across multiple regions.

### Future Improvements

1. **Expand to Full 15-Test Suite:**
Add P1 tests (payment methods: Affirm, bank; timeout/failure paths).
Implement request interception for deterministic backend failure injection.
Add tests for cross-member data isolation (security boundary testing).

1. **API-Layer Automation:**
Create complementary API tests for the same flows to validate backend behavior independently.
Use API tests for bulk data validation, edge cases, and negative scenarios cheaper than UI tests.

1. **Visual Regression Testing:**
Add Playwright visual snapshots for booking confirmation page to catch unintended UI regressions.

1. **Test Reporting and Insights:**
Integrate test results into dashboards (e.g., via pytest-html with custom reporters).
Track test execution time, flakiness rates, and failure patterns over time.

1. **Cross-Device Testing:**
Currently tests run only on desktop (chromium).
Future: Add Firefox and WebKit execution to catch browser-specific issues.
Future: Add mobile device emulation for responsive design validation.

1. **Load and Performance Testing:**
Current suite validates functional correctness; does not measure performance.
Future: Implement Lighthouse integration or custom performance assertions for critical paths.

1. **Accessibility Testing:**
Add axe-core integration to validate WCAG compliance on critical user flows.

1. **Test Data Management:**
Implement a shared test data service or fixture factory to reduce duplication.
Add support for pre-created test users to enable test isolation without setup overhead.
Replace the single hardcoded area code with a vetted list of valid area codes and controlled selection to keep reliability while improving data realism.

1. **Environment Parameterization and Dynamic Config:**
Add an explicit environment parameter (for example: local, staging, production-like) to test execution.
Use env_config.py as the single source of truth to dynamically resolve URLs, credentials, and environment-specific settings.
Centralize environment switching logic to reduce hardcoded assumptions and simplify CI/CD configuration.

1. **Expand Base Page for Reusable Navigation/Wait Patterns:**
Move common synchronization and transition logic into base page helpers (for example: robust "wait for next page" patterns, resilient URL + element readiness checks, and retry-safe page transition utilities).
Reuse those helpers across page objects to reduce duplicate waiting logic and improve consistency in flow handling.

1. **Mobile Automation Roadmap (Appium):**
Prepare a future mobile automation path using Appium for native mobile coverage when a mobile app exists.
In the meantime, continue mobile web validation via Playwright device emulation until native app surfaces are available.

### Question 1, Part 1: 15 Registration Tests Ranked by Priority

1. **P0** - Register new member with valid credit card for MRI Scan
2. **P0** - Declined credit card blocks registration completion
3. **P0** - Successful credit card payment but registration fails (safe roll-back of charge)
4. **P0** - Required registration fields blocks registration completion
5. **P1** - Register new member with Affirm for MRI Scan with Skeletal and Neurological Assessment
6. **P1** - Register with bank account for Lung Scan
7. **P1** - Register for user and upsell from MRI Scan to MRI Scan with Skeletal when selecting scan location
8. **P1** - Expired credit card blocks registration completion
9. **P1** - Insufficient funds card blocks registration
10. **P1** - Affirm authorization failure blocks registration completion
11. **P1** - Bank authorization failure blocks registration completion
12. **P1** - Newly registered user can sign back in successfully
13. **P1** - Duplicate email address is prevented
14. **P2** - Register then complete medical questionnaire successfully
15. **P2** - Register member and selecting back button without losing data

### Question 1, Part 2: Why These 3 Tests Are Most Important

These tests provide the highest confidence that the system correctly handles payments and booking integrity, which represents the highest-risk failure domain due to its direct impact on revenue, user trust, and downstream operational correctness.

#### P0 - Register new member with valid credit card for MRI Scan

This test validates the primary happy-path booking flow. It is ranked as most important because it confirms that a user can successfully complete the core revenue-generating workflow end-to-end. This test ensures that a successful payment results in a correctly created and confirmed booking that matches the user's selections during registration.

#### P0 - Declined credit card blocks registration completion

This test verifies that the system correctly handles failed payment authorization and prevents bookings from being created without valid payment. If declines are not enforced properly, it can result in unpaid services, reconciliation issues, or inconsistent system state. Credit card decline is prioritized over other payment failures because it is the most commonly used payment method and provides broad coverage of payment-failure handling logic.

#### P0 - Successful credit card payment but registration fails (safe roll-back of charge)

This test protects against one of the highest-impact system failures: a successful charge without a corresponding booking. This scenario can lead to direct financial disputes, loss of customer trust, and significant support overhead. Validating correct rollback or compensation behavior when booking creation fails after payment ensures transactional integrity between the payment and booking systems.

### Question 2, Part 1: Integration Test Case for Data Isolation

#### Integration Test: Second user is not able to access first user's medical questionnaire

**Test Setup:**

- Create 2 members

**Test Steps:**

1. Member A partially completes medical questionnaire
2. Member B attempts to access Member A's medical questionnaire through the API using Member B's authorization on the request

**Expected Result:**

- The request is rejected
- No medical data is returned
- Authorization is enforced at the API layer, not via UI routing

### Question 2, Part 2: HTTP Request for Integration Test

```bash
curl --location 'https://stage-api.ezra.com/diagnostics/api/medicaldata/forms/mq/submissions/{{MEMBER_A_SUBMISSION_ID}}/data' \
  --header 'Authorization: Bearer {{MEMBER_B_BEARER_TOKEN}}'
```

This curl demonstrates Member B attempting to access Member A's medical information by using a GET request for the medical question submission data using Member A's submission ID with Member B's bearer token. The specific endpoint may vary, but this request illustrates the authorization boundary being tested.

### Question 3: Security Testing Strategy for Sensitive Endpoints

With many endpoints handling sensitive data, the primary trade-off is security confidence versus development velocity. Attempting to test everything would slow delivery and create a false sense of security, so the focus should be on enforcing and validating system-level guarantees rather than endpoint-by-endpoint coverage.

**Risk-Based Approach:**

1. **Classify by sensitivity:** Group endpoints by data classification—medical data, PII, and payment data.
2. **Identify shared behavior:** Find authorization and access-control patterns across categories.
3. **Target representative endpoints:** Test core authorization invariants across high-risk categories rather than duplicating tests for each endpoint.
4. **Cross-member access validation:** Implement a small number of high-signal integration tests that intentionally attempt cross-member access using valid authentication tokens.

**Mitigations:**

This approach relies on centralized authorization being consistently applied and not bypassed by individual endpoints. To mitigate that risk:

- Pair this testing strategy with architectural enforcement of authorization
- Implement targeted code reviews for data access changes
- Deploy monitoring to detect anomalous access patterns

While this does not eliminate all risk, it provides scalable, defensible security coverage without significantly impacting development velocity.
