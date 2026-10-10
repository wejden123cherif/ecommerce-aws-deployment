# Logging, Monitoring and Alerting Configuration

## 1. AWS CloudTrail

Trail:

```text
ecommerce-security-audit-trail
```

Observed configuration:

- logging active
- multi-region: Yes
- organisation trail: No
- S3 log delivery active
- recursive logging enabled
- log file validation disabled
- CloudTrail log files not configured with a customer-managed KMS key

The S3 bucket itself uses SSE-S3 encryption, therefore lack of CloudTrail KMS CMK configuration does not mean the log files are stored unencrypted.

## 2. CloudTrail to CloudWatch Logs

The audit team attempted to configure CloudTrail integration with the existing CloudWatch log group. The Learner Lab role returned `AccessDeniedException` for `iam:AttachRolePolicy` on the required role.

This is documented as a Learner Lab permission limitation under T-07 / EV-007 rather than as proof that CloudTrail itself is disabled.

## 3. CloudWatch log groups

Eight visible log groups were observed, including:

- `/aws/rds/instance/database-1/postgresql`
- Elastic Load Balancing vended logs
- `ecommerce-cloudtrail-logs`
- `logs_ec2`
- Lambda-related log groups

Visible log groups used the Standard log class and showed `Never expire` retention in the console view.

## 4. Metrics

Observed metrics included:

- EC2 CPUUtilization
- EC2 NetworkIn
- ALB TargetResponseTime
- ALB Requests
- ALB Rule Evaluations

These demonstrate that infrastructure monitoring is operational.

## 5. RDS logging

RDS CloudWatch log publication included:

- PostgreSQL log
- IAM database authentication error log

Database Insights Standard was enabled. Enhanced Monitoring was disabled.

## 6. CloudWatch alarm

Alarm:

```text
Name: EC2 failed
Namespace: AWS/EC2
Metric: StatusCheckFailed
Instance: i-03687e15b74af60a4
Statistic: Average
Period: 5 minutes
Datapoints to alarm: 1 of 1
Actions: enabled
```

The alarm is configured to send a message to SNS topic:

```text
ecommerce-security-alerts
```

## 7. SNS

The SNS subscription was confirmed. This establishes the observed alert chain:

```text
EC2 StatusCheckFailed
  → CloudWatch alarm
  → SNS ecommerce-security-alerts
  → confirmed subscriber
```

Prowler reported that the SNS topic does not use KMS encryption at rest. This is retained as a hardening observation and does not invalidate the operational notification chain.
