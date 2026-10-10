# T-02 — Identities and Access

**Test ID:** T-02  
**Audit criterion:** G-02 — documented project requirement mapped to A.5.15  
**ISO control:** ISO/IEC 27001:2022 A.5.15  
**Audit question:** Are access rights limited and strong application authentication enabled?  
**Method:** Manual IAM/Cognito review and scanner correlation

## Resources examined

Visible IAM roles/policies; temporary STS role; Cognito user pool izmaco and admin group.

## Evidence reference

Primary group: [EV-002](../08_Evidence/EV-002_IAM_Access_Control/README.md). Cross-tool support: [EV-006](../08_Evidence/EV-006_Security_Scan/README.md); environment qualifications: [EV-007](../08_Evidence/EV-007_Lab_Limitations/README.md). Documentary execution source: Session 2 (`../09_Test_Results/Session_2_Final_Audit_Execution.docx`; private source). File-level paths and hashes are in the evidence register and traceability matrix.

## Findings/observations

F-03 (Minor / Medium); platform-managed IAM observations separated. Cognito MFA evidence supports F-03. IAM listings do not prove least privilege or the upstream Academy MFA state.

**Control:** A.5.15  
**Evidence:** EV-002  
**Result:** PARTIAL  
**Classification:** Minor nonconformity

## Procedure executed
The team reviewed the AWS Learner Lab assumed-role access model, visible IAM configuration, Cognito authentication settings, application admin-group authorization and Prowler/ScoutSuite identity findings.

## Observed result
AWS administration is performed through temporary STS credentials under the Vocareum/AWS Academy model rather than through a permanent IAM user created by the team. Cognito authenticates application users and an admin group is used for privileged application authorization. Cognito MFA enforcement is configured as **No MFA**.

Prowler also reported elevated privileges on the Vocareum-managed role and several account-level IAM observations. These are not attributed to the e-commerce team where they are clearly platform/lab managed. ScoutSuite password-policy findings are retained as account-level scanner observations, but the audited administrative access path uses temporary assumed-role credentials and IAM user creation is explicitly denied in the lab.

## Conclusion
Access controls exist, but strong authentication is not fully enforced for Cognito users. This is recorded as a minor nonconformity. Learner Lab IAM restrictions are recorded under T-07.
