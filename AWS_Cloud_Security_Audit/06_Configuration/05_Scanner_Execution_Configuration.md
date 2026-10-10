# Scanner Execution Configuration

## 1. Target

Both scanners were executed against:

```text
AWS Account: 623463264556
Region: us-east-1
Authentication: AWS Academy/Vocareum temporary STS assumed role
```

## 2. Prowler

Prowler version:

```text
5.44.0
```

Executed service scope:

```text
iam ec2 vpc rds s3 cloudtrail cloudwatch cognito elbv2 wafv2 secretsmanager kms sns
```

Command:

```bash
prowler aws \
  --services iam ec2 vpc rds s3 cloudtrail cloudwatch cognito elbv2 wafv2 secretsmanager kms sns \
  --region us-east-1 \
  -M html csv json-ocsf \
  -o ./prowler-results
```

Output formats:

- HTML
- CSV
- OCSF JSON

The CSV output uses semicolon delimiters and contains multiline quoted fields.

## 3. ScoutSuite

ScoutSuite was installed in a dedicated virtual environment and executed against the same account. The report was generated under:

```text
./scoutsuite-results/
```

Primary files retained:

```text
ecommerce-security-audit.html
scoutsuite_results_ecommerce-security-audit.js
scoutsuite_errors_ecommerce-security-audit.json
scoutsuite_exceptions_ecommerce-security-audit.js
```

The report was viewed using a local HTTP server and evidence screenshots were captured from the local dashboard.

## 4. Scanner interpretation rule

Automated findings are not counted automatically as separate audit nonconformities. They are correlated with:

- manual AWS configuration evidence
- resource ownership and project scope
- AWS Academy/Vocareum permission limitations
- duplicate checks describing the same root cause

For example, multiple Prowler checks for SSH exposure are consolidated into the single T-04 finding concerning EC2 TCP/22 from `0.0.0.0/0`.
