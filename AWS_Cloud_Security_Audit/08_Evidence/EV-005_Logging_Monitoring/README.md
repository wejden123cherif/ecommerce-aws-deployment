# EV-005 — Logging Monitoring

**Evidence ID:** EV-005\
**Related test:** T-05 / G-05\
**ISO control:** ISO/IEC 27001:2022 A.8.9

## What the evidence supports

Active multi-region CloudTrail, delivered log objects, visible CloudWatch metrics/log groups and configured alarm/SNS subscription.

## Supporting artifacts

Console captures and raw scanner exports are held privately.

- `EV005-01_CloudTrail_Trails_Overview.png`
- `EV005-02_CloudTrail_Trail_Active_MultiRegion.png`
- `EV005-03_CloudWatch_Log_Groups.png`
- `EV005-04_ALB_Monitoring_Metrics.png`
- `EV005-05_CloudWatch_EC2_Metrics.png`
- `EV005-06_CloudWatch_Alarm_Overview.png`
- `EV005-07_CloudWatch_EC2_Alarm_Configuration.png`
- `EV005-08_CloudWatch_Alarm_SNS_Action.png`
- `EV005-09_SNS_Subscription_Confirmed.png`

## Interpretation limits

The notification configuration and subscription are evidenced; an actual alarm-triggered delivery test is not retained. Disabled validation and unspecified retention support F-04/F-05.

See [evidence handling](../Evidence_Handling.md) for source provenance and access to supporting artifacts.
