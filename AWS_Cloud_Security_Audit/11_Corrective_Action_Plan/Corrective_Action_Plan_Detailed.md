# Corrective Action Plan — Detailed Notes

## Priority model
- **P1 — Immediate:** High-risk exposure or encryption gap that should be addressed before production-like use.
- **P2 — Short term:** Material security improvement to implement in the next configuration cycle.
- **P3 — Planned hardening:** Lower-risk or defense-in-depth improvement.

## P1 actions
### AC-01 — Restrict SSH
Linked finding: F-01. Remove TCP/22 from `0.0.0.0/0`. Prefer a managed administrative mechanism or a narrow trusted source. Do not remove the rule until an alternative administration path is verified in the lab.

### AC-02 — Encrypt EC2 EBS
Linked finding: F-02. Use a safe snapshot/copy/replace procedure to migrate to encrypted storage. Enable EBS encryption by default if the Learner Lab exposes that account setting. Preserve application availability and evidence before migration.

## P2 actions
### AC-03 — Enforce Cognito MFA
Prioritize administrators and privileged users. Validate enrollment, recovery and successful login after the change.

### AC-06 — Add account-level S3 guardrail
The existing CloudTrail bucket is already protected. This action prevents future buckets from being accidentally exposed.

### AC-07 — Encrypt SNS topic
Apply KMS encryption to `ecommerce-security-alerts` if allowed by the lab. Re-test CloudWatch alarm delivery afterward.

### AC-08 — Strengthen RDS resilience
Treat Single-AZ and backup findings according to the educational lab's cost/capacity limitations. At minimum document acceptable retention and recovery expectations.

## P3 actions
### AC-04 — Enable CloudTrail validation
Strengthens forensic integrity without changing the fact that the trail is already operational.

### AC-05 — Define log retention
Replace undefined `Never expire` behavior with an approved policy if required by project governance.

### AC-09 — Remove stale RDS rule
Do not remove TCP/5543 until its purpose has been checked. If unused, delete it and preserve before/after evidence.

### AC-10 — Network telemetry and NACL review
Enable VPC Flow Logs where permissions and cost constraints permit. Keep security groups as the primary workload filtering layer and use NACLs as an additional boundary where justified.
