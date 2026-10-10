# EV-002 — IAM Access Control

**Evidence ID:** EV-002\
**Related test:** T-02 / G-02\
**ISO control:** ISO/IEC 27001:2022 A.5.15

## What the evidence supports

Visible IAM role/policy inventory, Cognito users/groups and No MFA configuration.

## Supporting artifacts

Console captures and raw scanner exports are held privately.

- `EV002-01_IAM_Roles_Overview.png`
- `EV002-02_IAM_Roles_Additional.png`
- `EV002-03_IAM_Policies_Overview.png`
- `EV002-04_Cognito_User_Pool_Users.png`
- `EV002-05_Cognito_Groups.png`
- `EV002-06_Cognito_Admin_Group_Member.png`
- `EV002-07_Cognito_SignIn_MFA_No_MFA.png`

## Interpretation limits

Cognito MFA evidence supports F-03. IAM listings do not prove least privilege or the upstream Academy MFA state.

See [evidence handling](../Evidence_Handling.md) for source provenance and access to supporting artifacts.
