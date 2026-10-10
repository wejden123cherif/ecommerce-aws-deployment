# ScoutSuite Installation and Validation

## 1. Purpose

ScoutSuite was used as a second automated configuration assessment tool to complement Prowler and strengthen T-06 / EV-006 evidence.

## 2. Separate virtual environment

Prowler and ScoutSuite were intentionally isolated from each other.

```bash
deactivate 2>/dev/null || true
python3 -m venv ~/scoutsuite-venv
source ~/scoutsuite-venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install scoutsuite
```

Validation:

```bash
scout --version
aws sts get-caller-identity
```

## 3. ScoutSuite report directory

The ScoutSuite working directory was:

```text
~/AWS_Audit/EV-006_ScoutSuite/
```

The scan generated a report directory containing, among other files:

```text
scoutsuite-results/ecommerce-security-audit.html
scoutsuite-results/scoutsuite-results/scoutsuite_results_ecommerce-security-audit.js
scoutsuite-results/scoutsuite-results/scoutsuite_errors_ecommerce-security-audit.json
scoutsuite-results/scoutsuite-results/scoutsuite_exceptions_ecommerce-security-audit.js
```

## 4. Local report viewing

The HTML report was viewed locally without publishing it to the Internet:

```bash
cd ~/AWS_Audit/EV-006_ScoutSuite
python3 -m http.server 8000 --directory ./scoutsuite-results
```

The report was then opened in the local browser at:

```text
http://localhost:8000/ecommerce-security-audit.html
```

The local HTTP server was stopped after evidence capture with `Ctrl+C`.

## 5. Evidence captured

ScoutSuite evidence includes:

- dashboard overview
- CloudTrail findings
- CloudWatch findings
- EC2 findings
- KMS findings
- RDS findings
- IAM findings
- VPC findings
- raw ScoutSuite report files

The Session 2 record includes dashboard images. Standalone captures supporting EV-006 are retained with the scanner evidence.
