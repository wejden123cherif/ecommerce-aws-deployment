# Detailed Audit Findings

## F-01 — Internet-exposed SSH administration
**Test:** T-04  
**Control:** A.8.9  
**Classification:** Major nonconformity  
**Risk:** High

EC2 security group `sg-045fb00f9aadc1d96` permits TCP/22 from `0.0.0.0/0` to instance `i-03687e15b74af60a4`. The condition was first identified through manual security-group review and independently corroborated by Prowler and ScoutSuite.

**Risk:** Broad Internet exposure of the administrative SSH service increases brute-force, credential-theft and remote-access attack surface.

**Recommendation:** Remove the Internet-wide SSH rule. Use a restricted trusted source or a managed administrative path such as AWS Systems Manager Session Manager when available and permitted.

---

## F-02 — Unencrypted EC2 EBS storage
**Test:** T-03  
**Control:** A.8.9  
**Classification:** Major nonconformity  
**Risk:** High

Prowler and ScoutSuite both report the audited EC2 EBS volume as unencrypted. Both also identify that EBS encryption by default is disabled for the account/region configuration.

**Risk:** Data on EC2 block storage is not protected by encryption at rest if the scanner result reflects the current volume state.

**Recommendation:** Encrypt the EC2 volume using an approved migration/snapshot process and enable EBS encryption by default for future volumes where the Learner Lab permissions allow it.

---

## F-03 — Cognito MFA not enforced
**Test:** T-02  
**Control:** A.5.15  
**Classification:** Minor nonconformity  
**Risk:** Medium

The Cognito user pool authentication configuration shows MFA enforcement set to `No MFA`.

**Risk:** Password compromise alone may be sufficient to authenticate an application user, including potentially privileged users if no compensating factor is required.

**Recommendation:** Enforce or appropriately require MFA for privileged users and, where feasible, for all application users based on the project's risk profile.

---

## F-04 — CloudTrail log-file validation disabled
**Test:** T-05  
**Control:** A.8.9  
**Classification:** Observation  
**Risk:** Low

CloudTrail log-file validation is disabled. Logging itself is active and files are successfully delivered to S3.

**Recommendation:** Enable log-file validation where permitted to strengthen integrity verification of CloudTrail log files.

---

## F-05 — No explicit CloudWatch retention policy
**Test:** T-05  
**Control:** A.8.9  
**Classification:** Observation  
**Risk:** Low

Visible CloudWatch log groups are configured with `Never expire`, and no project-specific retention period has been documented.

**Recommendation:** Define a retention policy that balances forensic requirements, privacy, cost and academic-lab constraints, then configure log-group retention accordingly.

---

## F-06 — S3 account-level public-access guardrail absent
**Test:** T-03  
**Control:** A.8.9  
**Classification:** Observation  
**Risk:** Medium

Prowler reports that account-level S3 Block Public Access is not configured. The audited CloudTrail S3 bucket itself has bucket-level Block Public Access enabled and is therefore not being reported as public.

**Recommendation:** Enable account-level S3 Block Public Access when compatible with the lab and application requirements, while retaining bucket-level protections.

---

## F-07 — SNS topic not KMS-encrypted according to Prowler
**Test:** T-05  
**Control:** A.8.9  
**Classification:** Observation  
**Risk:** Medium

Prowler reports that SNS topic `ecommerce-security-alerts` does not meet the KMS encryption-at-rest check. The alert path itself is operational and a subscription was confirmed.

**Recommendation:** Enable SNS server-side encryption with KMS where allowed and where the sensitivity of notification content justifies it.

---

## F-08 — RDS resilience and backup hardening
**Test:** T-03  
**Control:** A.8.9  
**Classification:** Observation  
**Risk:** Medium

ScoutSuite reports a Single-AZ RDS instance and short backup retention. Prowler reports that `database-1` is not protected by an AWS Backup plan. These observations concern resilience and recovery rather than the already-verified RDS storage encryption.

**Recommendation:** Define the required recovery objectives, increase retention where appropriate, and consider Multi-AZ/AWS Backup protections outside the cost and service limits of the educational lab.

---

## F-09 — Potential stale RDS TCP/5543 rule
**Test:** T-04  
**Control:** A.8.9  
**Classification:** Observation  
**Risk:** Low

The additional `RDS sg` security group allows TCP/5543 from the EC2 security group, while the verified PostgreSQL service and linked RDS security-group path use TCP/5432.

**Recommendation:** Confirm whether TCP/5543 is used by any legitimate component. Remove the rule if it has no documented purpose.

---

## F-10 — Permissive default NACL posture and missing Flow Logs
**Test:** T-04  
**Control:** A.8.9  
**Classification:** Observation  
**Risk:** Medium

ScoutSuite reports default NACLs allowing broad ingress/egress and subnets without VPC Flow Logs. Security groups still provide the principal workload-level filtering, so this is treated as a defense-in-depth observation rather than evidence that every port is publicly reachable.

**Recommendation:** Review NACL necessity and enable VPC Flow Logs for relevant subnets/VPC where permissions and cost constraints allow.
