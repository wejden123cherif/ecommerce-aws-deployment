# T-07 — AWS Academy Learner Lab Limitations

**Test ID:** T-07  
**Audit criterion:** G-07 — documented project requirement mapped to A.8.9  
**ISO control:** ISO/IEC 27001:2022 A.8.9  
**Audit question:** Are AWS Academy Learner Lab limitations documented and separated from project findings?  
**Method:** Documentary and permission-denial review with primary/secondary source distinction

## Resources examined

AWS Academy/Vocareum assumed-role access; IAM CreateUser and AttachRolePolicy denials; CloudTrail console denial; scanner visibility; secondary session narratives.

## Evidence reference

Primary group: [EV-007](../08_Evidence/EV-007_Lab_Limitations/README.md). Cross-tool support: [EV-006](../08_Evidence/EV-006_Security_Scan/README.md); environment qualifications: [EV-007](../08_Evidence/EV-007_Lab_Limitations/README.md). Documentary execution source: Session 2 (`../09_Test_Results/Session_2_Final_Audit_Execution.docx`; private source). File-level paths and hashes are in the evidence register and traceability matrix.

## Findings/observations

No application nonconformity raised for platform restrictions or local tooling. RDS capacity, a Vocareum restart and local WSL failure are secondary session narratives with missing primary artifacts. AWS session expiry is an access-model constraint; no direct expiry capture is retained.

**Control:** A.8.9  
**Evidence:** EV-007  
**Result:** COMPLETED  
**Classification:** Compliant — limitations documented

## Procedure executed

Reviewed the assumed-role and AccessDenied captures, the Prowler policy-visibility message and ScoutSuite error file. Assessed Session 2 narratives separately where primary captures were unavailable.

## Observed result

### Documented limitations
- AWS access is provided through temporary Vocareum/AWS Academy STS assumed-role credentials.
- IAM user creation is denied (`iam:CreateUser`).
- Attaching the policy required for the attempted CloudTrail-to-CloudWatch Logs integration is denied (`iam:AttachRolePolicy`).
- Some CloudTrail console resources return AccessDenied.
- Prowler explicitly reports that some policy checks may be inconclusive because access is denied to the `voclabs` role.
- RDS start operation encountered a provider capacity error for `db.t4g.micro` in `us-east-1a`.
- CloudTrail recorded an EC2 `StartInstances` action under a Vocareum assumed role, indicating lab/platform-managed behavior; the exact internal Vocareum workflow is not asserted.
- A local WSL read-only/I/O failure interrupted the first Prowler installation attempt; this is a tooling limitation rather than an AWS security finding.

## Conclusion
The limitations are documented. Direct evidence supports assumed-role access and explicit permission denials; the provider-capacity, restart and WSL incidents are secondary narrative records without retained primary artifacts. T-07 is compliant.
