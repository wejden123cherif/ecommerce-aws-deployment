# Storage, Identity and Secrets Configuration

## 1. RDS storage

Observed RDS configuration:

- storage encryption enabled
- AWS managed KMS key `aws/rds`
- credentials managed through AWS Secrets Manager
- PostgreSQL port 5432
- private database subnet structure
- Multi-AZ disabled
- deletion protection disabled

Automated scanners additionally identified backup/resilience observations. These are analysed in Session 2 rather than treated as proof that RDS storage is unencrypted.

## 2. CloudTrail S3 bucket

CloudTrail logs are delivered to:

```text
aws-cloudtrail-logs-623463264556-30cad2de
```

Observed bucket controls:

- Block Public Access: On at bucket level
- default encryption: SSE-S3
- CloudTrail log objects observed under the account/region/date hierarchy

Prowler separately reported that account-level S3 Block Public Access is not configured. This is an account-wide guardrail observation and does not mean the verified CloudTrail bucket is public.

## 3. EC2 EBS storage

Both Prowler and ScoutSuite reported that the EBS volume associated with the audited EC2 environment is not encrypted and that EBS encryption-by-default is disabled. This is treated as a storage configuration nonconformity in Session 2.

## 4. Cognito

Amazon Cognito User Pool:

```text
User pool: User pool - izmaco
Sign-in identifier: Email
Password authentication: enabled
MFA enforcement: No MFA
```

The application uses Cognito group-based authorization, including an `admin` group used by backend authorization logic.

## 5. AWS administrative identity

The AWS Academy Learner Lab does not provide a permanent IAM administrator user to the audit team. Console and CLI access are delivered through a temporary STS assumed role controlled by AWS Academy/Vocareum.

Permission denials encountered during the audit are recorded under T-07 / EV-007.

## 6. Secrets Manager

The RDS master credentials are stored in AWS Secrets Manager. Prowler reported that the secret did not have a restrictive resource policy **or** that the `voclabs` role lacked permission to inspect that policy. Because the scanner result is explicitly ambiguous, it is retained as an observation requiring manual context rather than a confirmed insecure secret policy.
