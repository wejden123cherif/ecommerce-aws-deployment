# EV-003 — Storage Security

**Evidence ID:** EV-003\
**Related test:** T-03 / G-03\
**ISO control:** ISO/IEC 27001:2022 A.8.9

## What the evidence supports

RDS encryption and Secrets Manager integration; S3 bucket-level public-access blocking and SSE-S3 encryption.

## Supporting artifacts

Console captures and raw scanner exports are held privately.

- `EV003-01_RDS_Connectivity_SecretsManager.png`
- `EV003-02_RDS_Configuration_Encryption.png`
- `EV003-03_RDS_Maintenance_Backup_Settings.png`
- `EV003-04_CloudTrail_S3_Bucket_Objects.png`
- `EV003-05_CloudTrail_S3_Log_Objects.png`
- `EV003-06_CloudTrail_S3_Block_Public_Access.png`
- `EV003-07_CloudTrail_S3_Default_Encryption.png`

## Interpretation limits

F-02 EBS encryption and F-06 account-level S3 findings require EV-006 raw scanner evidence. The RDS maintenance screenshot does not display backup retention.

See [evidence handling](../Evidence_Handling.md) for source provenance and access to supporting artifacts.
