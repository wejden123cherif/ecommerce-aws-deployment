# T-05 — Logging, Monitoring and Alerting

**Test ID:** T-05  
**Audit criterion:** G-05 — documented project requirement mapped to A.8.9  
**ISO control:** ISO/IEC 27001:2022 A.8.9  
**Audit question:** Are logging, monitoring and alerting operational?  
**Method:** Manual CloudTrail/CloudWatch/SNS review and scanner correlation

## Resources examined

CloudTrail ecommerce-security-audit-trail; CloudTrail S3 bucket; reviewed CloudWatch log groups/metrics; alarm EC2 failed; SNS ecommerce-security-alerts.

## Evidence reference

Primary group: [EV-005](../08_Evidence/EV-005_Logging_Monitoring/README.md). Cross-tool support: [EV-006](../08_Evidence/EV-006_Security_Scan/README.md); environment qualifications: [EV-007](../08_Evidence/EV-007_Lab_Limitations/README.md). Documentary execution source: Session 2 (`../09_Test_Results/Session_2_Final_Audit_Execution.docx`; private source). File-level paths and hashes are in the evidence register and traceability matrix.

## Findings/observations

F-04, F-05 and F-07 (observations); collection/integration limits under T-07. The notification configuration and subscription are evidenced; an actual alarm-triggered delivery test is not retained. Disabled validation and unspecified retention support F-04/F-05.

**Control:** A.8.9  
**Evidence:** EV-005  
**Result:** PASS WITH OBSERVATIONS  
**Classification:** Compliant with observations

## Procedure executed
The team reviewed CloudTrail, S3 delivery, CloudWatch log groups, EC2/ALB metrics, CloudWatch alarms, SNS actions/subscription, RDS log publication and scanner findings.

## Observed result
- CloudTrail `ecommerce-security-audit-trail` is actively logging and is multi-region.
- CloudTrail log files are delivered to the dedicated S3 bucket.
- CloudWatch log groups exist and RDS PostgreSQL logs are published.
- EC2 and ALB metrics show collected data.
- Alarm `EC2 failed` monitors `StatusCheckFailed` and sends notifications to SNS topic `ecommerce-security-alerts`.
- SNS subscription confirmation was evidenced.

Observations:
- CloudTrail log-file validation is disabled.
- Visible CloudWatch log groups use `Never expire`, with no explicit project retention period documented.
- ScoutSuite reports that the trail is not integrated with CloudWatch Logs. An attempted integration was blocked by the Learner Lab because `iam:AttachRolePolicy` was denied; this is recorded under EV-007 as a lab limitation.
- ScoutSuite reports that CloudTrail logging does not cover all data resources and that CloudTrail logs are not protected with a customer-managed KMS key. These are hardening observations, not evidence that logging is disabled.

## Conclusion
Logging, monitoring and alerting are operational. T-05 passes with observations.
