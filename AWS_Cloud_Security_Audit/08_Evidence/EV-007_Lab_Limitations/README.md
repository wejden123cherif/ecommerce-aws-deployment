# EV-007 — Lab Limitations

**Evidence ID:** EV-007\
**Related test:** T-07 / G-07\
**ISO control:** ISO/IEC 27001:2022 A.8.9

## What the evidence supports

Temporary assumed-role access and explicit permission denials for IAM/CloudTrail operations.

## Supporting artifacts

Console captures and raw scanner exports are held privately.

- `Limitations_Register.csv` — primary/secondary source disposition and IDs aligned with Session 2
- `EV007-01_LearnerLab_Assumed_Role_Evidence.png`
- `EV007-02_CloudTrail_CloudWatch_AttachRolePolicy_AccessDenied.png`
- `EV007-03_CloudTrail_Dashboard_AccessDenied.png`
- `EV007-04_IAM_CreateUser_AccessDenied.png`

## Interpretation limits

RDS capacity, a Vocareum restart and local WSL failure are secondary session narratives with missing primary artifacts. AWS session expiry is an access-model constraint; no direct expiry capture is retained.

See [evidence handling](../Evidence_Handling.md) for source provenance and access to supporting artifacts.
