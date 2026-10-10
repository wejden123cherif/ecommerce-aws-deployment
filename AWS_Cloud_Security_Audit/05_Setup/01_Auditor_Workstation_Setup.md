# Auditor Workstation Setup

## 1. Objective

Prepare an isolated local workstation capable of authenticating to the AWS Academy Learner Lab and running cloud configuration assessment tools without installing audit dependencies globally.

## 2. Workstation baseline

The audit workstation used:

- Ubuntu 24.04.4 LTS under WSL
- Python 3.12
- Python `venv`
- pip
- AWS CLI
- local file storage for raw scanner reports and screenshots

## 3. Basic validation commands

```bash
python3 --version
pip --version
aws --version
```

The Python version used by the scanner environments was Python 3.12.

## 4. Working directory

The audit working area was organised under:

```text
~/AWS_Audit/
```

Scanner evidence was separated into:

```text
~/AWS_Audit/EV-006_Prowler/
~/AWS_Audit/EV-006_ScoutSuite/
```

## 5. Why AWS CloudShell was not retained

AWS CloudShell was evaluated but was not retained as the main scanner workstation because the observed environment had Python 3.13 and only approximately 906 MB of free storage. The local WSL environment provided more control over Python versions, virtual environments and report retention.

## 6. Local workstation limitation encountered

During the first Prowler installation attempt, the WSL filesystem temporarily became read-only and commands returned I/O errors. This caused an incomplete dependency installation and later an import error. The issue was treated as a local tooling limitation rather than an AWS security finding.

The recovery approach was:

1. Restore a stable writable WSL filesystem.
2. Discard the inconsistent Prowler virtual environment.
3. Create a fresh Python virtual environment.
4. Reinstall Prowler from a clean state.
5. Validate the installation before starting the audit scan.

This limitation is also referenced under T-07 / EV-007 because it affected audit tooling but not the audited AWS configuration.
