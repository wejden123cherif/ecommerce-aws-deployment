# T-03 — Storage Security

**Test ID:** T-03  
**Audit criterion:** G-03 — documented project requirement mapped to A.8.9  
**ISO control:** ISO/IEC 27001:2022 A.8.9  
**Audit question:** Is scoped storage protected from public exposure and appropriately encrypted?  
**Method:** Manual RDS/S3 review and scanner correlation

## Resources examined

RDS database-1; its Secrets Manager reference; CloudTrail S3 bucket; EBS vol-0b10c9d68b59e72af attached to i-03687e15b74af60a4.

## Evidence reference

Primary group: [EV-003](../08_Evidence/EV-003_Storage_Security/README.md). Cross-tool support: [EV-006](../08_Evidence/EV-006_Security_Scan/README.md); environment qualifications: [EV-007](../08_Evidence/EV-007_Lab_Limitations/README.md). Documentary execution source: Session 2 (`../09_Test_Results/Session_2_Final_Audit_Execution.docx`; private source). File-level paths and hashes are in the evidence register and traceability matrix.

## Findings/observations

F-02 (Major / High), F-06 and F-08 (observations). F-02 EBS encryption and F-06 account-level S3 findings require EV-006 raw scanner evidence. The RDS maintenance screenshot does not display backup retention.

**Control:** A.8.9  
**Evidence:** EV-003  
**Result:** PARTIAL  
**Classification:** Major nonconformity

## Procedure executed
The team reviewed RDS encryption and placement, S3 public-access controls and encryption, Secrets Manager usage, and automated scanner findings for EBS and account-level S3 controls.

## Observed result
Positive controls:
- RDS `database-1` storage encryption is enabled with the AWS-managed `aws/rds` key.
- RDS is placed in private database networking and is reached through linked EC2/RDS security groups.
- RDS master credentials are stored in AWS Secrets Manager.
- The CloudTrail S3 bucket has bucket-level Block Public Access enabled and default SSE-S3 encryption.

Gap:
- Prowler and ScoutSuite both identify the EC2 EBS volume as not encrypted, and EBS encryption by default as disabled.

Additional observation:
- Prowler reports that account-level S3 Block Public Access is not configured. This does not mean the audited CloudTrail bucket is public; that bucket is independently protected at bucket level.

## Conclusion
The database and audited log bucket have appropriate storage protection, but unencrypted EC2 block storage creates a significant configuration gap. T-03 is therefore classified as a major nonconformity.
