# EV-006 — Security Scan

**Evidence ID:** EV-006\
**Related test:** T-06 / G-06\
**ISO control:** ISO/IEC 27001:2022 A.8.9

## What the evidence supports

Prowler and ScoutSuite report generation, attributable raw configuration results and service dashboard captures.

## Supporting artifacts

Console captures and raw scanner exports are held privately.

- `Prowler/Raw_Report/Prowler_Final_Report.html`, `Prowler_Final_Results.csv`, `Prowler_Final_OCSF.json`
- `Prowler/Raw_Report/Prior_Run/` — original earlier run
- `Prowler/Analysis/Prowler_Critical_High_Findings.csv` — original 28-row extraction
- `Prowler/Screenshots/` — execution, extraction and final summary
- `ScoutSuite/Raw_Report/ecommerce-security-audit.html` and all accompanying assets/results
- `ScoutSuite/Screenshots/EV006-S01` through `EV006-S08` — visually identified dashboards

## Interpretation limits

Successful scanning does not imply a secure environment. Failed check-resource rows require scope/ownership triage; collection errors and MANUAL rows limit assurance.

See [evidence handling](../Evidence_Handling.md) for source provenance and access to supporting artifacts.
