# Contributing

Humanifest protects maintainers from speculative AI-generated contribution noise. Contributions here should model that standard.

Before opening nontrivial work:

1. Open or identify an issue.
2. Confirm the maintainer wants the work.
3. Keep the change narrow and explainable.
4. Include tests or a clear reason tests do not apply.
5. Disclose AI assistance and retain human responsibility.

Do not submit mass formatting, dependency churn, broad rewrites, automated issue reports, or unsolicited AI-generated PR reviews.

Code contributions are accepted under the repository license. Contributors should use DCO signoff unless the project later adopts a CLA.

## Development checks

The core suite and record checks run without third-party dependencies:

```bash
python3 -m unittest
python3 -m humanifest.cli validate --root .
python3 -m humanifest.cli report --root .
```

For the full CI checks, use a virtual environment and install the development
tools, then validate schemas and the installed package:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-checks.txt
.venv/bin/python -m scripts.check_schemas
.venv/bin/python -m scripts.check_install
```

The installation check builds a wheel with the installed build backend, creates a
temporary virtual environment, and runs every CLI command outside the checkout.
It uses no package index during build or installation and removes its temporary
environment afterward. Build artifacts in the checkout are ignored by Git.

CI runs these checks on Python 3.11 and 3.14 for pushes to `main` and pull requests.
It also compares `portfolio/status.md` with current report output. Refresh that
generated file using the README command whenever records or report formatting
change. CI has read-only repository permissions and does not contact maintainers,
publish packages, or change records.
