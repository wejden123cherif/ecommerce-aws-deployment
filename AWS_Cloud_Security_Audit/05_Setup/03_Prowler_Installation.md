# Prowler Installation and Validation

## 1. Purpose

Prowler was installed to perform an automated AWS configuration assessment for T-06 / EV-006 and to corroborate manual findings from T-02 through T-05.

## 2. Dedicated virtual environment

```bash
python3 -m venv ~/prowler-venv
source ~/prowler-venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install prowler
```

## 3. Installed version

The successfully validated installation was:

```text
Prowler 5.44.0
```

Validation:

```bash
prowler --version
prowler aws --list-services
```

`prowler aws --list-services` completed successfully and listed 89 available AWS services.

## 4. Installation problems encountered

### 4.1 Read-only filesystem

The first installation attempt failed with a WSL filesystem error similar to:

```text
OSError: [Errno 30] Read-only file system
```

Other local commands also returned `Input/output error`. This was a local WSL/storage problem, not an AWS configuration issue.

### 4.2 Inconsistent dependency state

A partially installed environment subsequently produced an import error involving `alibabacloud_tea_openapi`. The virtual environment was recreated rather than trying to repair the inconsistent package state.

## 5. Final scan command

The successful audit scan used the relevant AWS services in `us-east-1` and generated HTML, CSV and OCSF JSON output:

```bash
prowler aws \
  --services iam ec2 vpc rds s3 cloudtrail cloudwatch cognito elbv2 wafv2 secretsmanager kms sns \
  --region us-east-1 \
  -M html csv json-ocsf \
  -o ./prowler-results
```

## 6. Final output

The final scan produced:

- HTML report
- semicolon-delimited CSV report
- OCSF JSON report

The overview contained:

- 467 resource/check results
- 342 passed
- 111 failed
- 14 MANUAL results
- 0 muted

Prowler execution is therefore considered successful for T-06. Security findings from the scan are analysed separately and are not treated as independent vulnerabilities without manual triage.
