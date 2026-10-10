# AWS CLI Authentication — AWS Academy Learner Lab

## 1. Authentication model

The audit did not use a permanent IAM user. AWS Academy/Vocareum supplied temporary AWS credentials which were used by the AWS CLI and the security scanners.

The authenticated account was:

```text
AWS Account ID: 623463264556
Region: us-east-1
```

The observed caller identity used an AWS STS assumed role under the Learner Lab / Vocareum model.

## 2. Validation command

```bash
aws sts get-caller-identity
```

The command was used before scanner execution to confirm that the CLI session was authenticated to the intended AWS account.

## 3. AWS CLI profile

The scanners used the AWS CLI `default` profile.

Configuration was reviewed with:

```bash
aws configure list
```

Temporary credential values are intentionally excluded from this repository and must never be copied into evidence screenshots, reports or source files.

## 4. Session-expiry handling

AWS Academy credentials are temporary. If a tool returns `ExpiredToken`, the correct action is to obtain a fresh Learner Lab credential set and validate it again with `aws sts get-caller-identity` before continuing.

## 5. Permission boundary

Successful AWS CLI authentication does not imply unrestricted AWS administrative privileges. The Learner Lab role produced explicit `AccessDenied` responses for some IAM and CloudTrail operations. Those restrictions are documented under T-07 / EV-007 as environment limitations.
