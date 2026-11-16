# QA Playground

[![tests](https://github.com/FranciscoLima18/qa-playground/actions/workflows/tests.yml/badge.svg)](https://github.com/FranciscoLima18/qa-playground/actions/workflows/tests.yml)
[![report](https://img.shields.io/badge/report-latest-blue)](https://franciscolima18.github.io/qa-playground/)

A public test automation portfolio: end-to-end web tests and API tests written in **Python** with **Playwright** and **pytest**, running in **GitHub Actions** on every push and every night, with the latest HTML report published to **GitHub Pages**.

All targets are public practice applications built for testing. No real or private systems are involved.

## What is tested

| Suite | Target | Covers |
|---|---|---|
| `tests/web/test_todomvc.py` | [TodoMVC demo](https://demo.playwright.dev/todomvc/) | Add, complete, filter and delete items; persistence after reload; empty input |
| `tests/web/test_saucedemo.py` | [Sauce Demo](https://www.saucedemo.com/) | Successful login, data-driven invalid logins, full checkout flow |
| `tests/api/test_booking.py` | [Restful-Booker](https://restful-booker.herokuapp.com/) | Health check, create/read/update/delete, auth rules, response schema |

## Design choices

- **Page Object Model** (`pages/`) keeps selectors out of the tests, so a UI change is fixed in one place.
- **Web-first assertions** (`expect(...)`) wait automatically instead of using sleeps, which keeps the suite stable.
- **One tool for UI and API:** API tests use Playwright's built-in request context, no extra HTTP library.
- **Self-cleaning test data:** each API test creates its own booking and deletes it afterwards.
- **Debuggable failures:** screenshots and Playwright traces are kept only when a test fails and uploaded as CI artifacts.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install --with-deps chromium

pytest                 # everything
pytest -m api          # API tests only
pytest -m web --headed # watch the browser
```

The HTML report is written to `reports/report.html`. To inspect a failed test's trace:

```bash
playwright show-trace test-results/<test-folder>/trace.zip
```

## Project structure

```
pages/            Page Objects (TodoMVC, Sauce Demo)
tests/web/        End-to-end UI tests
tests/api/        API tests
conftest.py       Shared fixtures (API client, auth token)
pytest.ini        Default options: browser, tracing, report
.github/workflows CI pipeline and report publishing
```

## Roadmap

- Allure reporting with history
- Visual regression checks
- Accessibility checks with axe-core
- Cross-browser runs (Firefox, WebKit)

---

Made by [Francisco Lima Grille](https://www.linkedin.com/in/francisco-lima-grille-61945b328) · Computer Engineering student and QA Automation apprentice.
