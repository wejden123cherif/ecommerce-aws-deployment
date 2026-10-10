# 05_Setup — Audit Workstation and Security Scanner Installation

## Purpose

This folder documents the installation and preparation of the auditor workstation used to assess the AWS Academy Learner Lab e-commerce environment. It records the software environment, AWS CLI authentication method, installation of Prowler and ScoutSuite, and installation constraints encountered during the audit.

The setup was performed on the auditor workstation and did not modify the audited AWS resources.

## Auditor Workstation

| Item | Observed configuration |
|---|---|
| Operating environment | Ubuntu 24.04.4 LTS under Windows Subsystem for Linux (WSL) |
| Python | 3.12 |
| pip | 24.0 at initial setup; upgraded inside scanner virtual environments |
| AWS access | AWS CLI using temporary AWS Academy Learner Lab credentials |
| AWS account | `<AWS_ACCOUNT_ID>` |
| Primary AWS region | `us-east-1` |
| Authentication model | AWS STS assumed role supplied by AWS Academy/Vocareum |
| Prowler | 5.44.0 |
| ScoutSuite | Installed in a separate Python virtual environment |

## Installation Principle

Prowler and ScoutSuite were installed in separate Python virtual environments to avoid dependency conflicts:

- `~/prowler-venv`
- `~/scoutsuite-venv`

Credential values are kept outside the repository. Supporting captures and scanner exports are handled under the [evidence policy](../08_Evidence/Evidence_Handling.md).

## Files in this folder

- `01_Auditor_Workstation_Setup.md` — workstation preparation and prerequisite checks.
- `02_AWS_CLI_Authentication.md` — Learner Lab CLI authentication and validation.
- `03_Prowler_Installation.md` — Prowler installation, validation and recovery notes.
- `04_ScoutSuite_Installation.md` — ScoutSuite installation and local report viewing.
- `05_Setup_Validation_Checklist.md` — final installation validation checklist.

## Final setup status

The audit workstation was successfully prepared. AWS CLI access to account `<AWS_ACCOUNT_ID>` was validated, Prowler 5.44.0 successfully executed and produced reports, and ScoutSuite successfully executed and produced an HTML findings report and raw result files.
