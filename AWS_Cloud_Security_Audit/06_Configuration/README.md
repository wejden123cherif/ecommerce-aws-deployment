# 06_Configuration — Audited AWS Configuration Baseline

## Purpose

This folder records the configuration baseline observed during the cloud security audit. It provides a concise technical inventory of the AWS Learner Lab resources that were inspected manually and/or by Prowler and ScoutSuite.

The information in this folder describes the observed configuration. Security conclusions and classifications are documented in Session 2 and the findings register.

## Environment baseline

| Item | Observed value |
|---|---|
| AWS account | `<AWS_ACCOUNT_ID>` |
| Region | `us-east-1` |
| Main VPC | `<VPC_ID>` |
| Additional VPC | `<VPC_ID>` |
| Main EC2 instance | `<EC2_INSTANCE_ID>` |
| Application Load Balancer | `ALB` |
| RDS database | `database-1` |
| RDS engine | PostgreSQL 18.3 |
| Authentication service | Amazon Cognito User Pool |
| Audit logging | AWS CloudTrail |
| Monitoring | Amazon CloudWatch |
| Alerting | Amazon SNS |
| Security scanners | Prowler 5.44.0 and ScoutSuite |

## Files in this folder

- `01_AWS_Environment_Baseline.md`
- `02_Network_and_Security_Groups.md`
- `03_Storage_Identity_and_Secrets.md`
- `04_Logging_Monitoring_and_Alerting.md`
- `05_Scanner_Execution_Configuration.md`
- `Resource_Inventory.csv`

## Configuration handling rule

The audit was performed primarily through read-only observation. Existing insecure states were documented before remediation. Configuration was not changed merely to make an audit criterion pass.
