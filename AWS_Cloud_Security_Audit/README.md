# AWS Cloud Security Audit

Academic audit of an e-commerce application deployed in an **AWS Academy Learner Lab**. The assessment uses ISO/IEC 27001:2022 controls **A.5.23 — cloud services**, **A.5.15 — access control**, and **A.8.9 — configuration management**. It evaluates the observed configuration and does not assert ISO certification.

**Authors:** Wejden Cherif and Maram Raboudi\
**Supervisor:** Mohamed Ali Hadhri\
**Audit period:** 9–10 October 2026\
**Region:** `us-east-1`

## Scope and method

The assessment covers cloud responsibilities, Cognito and IAM access, EBS/S3/RDS storage, VPC and security groups, logging and monitoring, and automated configuration scanning. AWS Academy/Vocareum permission restrictions are assessed separately from application findings.

Each result follows **criterion → control → test → evidence → result → finding**. The [Terms of Reference](01_Project_Scope/Terms_of_Reference_42.md) defines the boundaries; the [traceability matrix](02_Audit_Program/Final_Traceability_Matrix.csv) connects the assessment records.

## Results

| Test | Area | Result |
|---|---|---|
| [T-01](07_Audit_Tests/T01_Cloud_Governance.md) | Cloud governance | PASS |
| [T-02](07_Audit_Tests/T02_Identity_Access_Control.md) | Identity and access | PARTIAL |
| [T-03](07_Audit_Tests/T03_Storage_Security.md) | Storage security | PARTIAL |
| [T-04](07_Audit_Tests/T04_Network_Security.md) | Network security | PARTIAL |
| [T-05](07_Audit_Tests/T05_Logging_Monitoring.md) | Logging and monitoring | PASS WITH OBSERVATIONS |
| [T-06](07_Audit_Tests/T06_Automated_Security_Scanning.md) | Automated scanning | PASS |
| [T-07](07_Audit_Tests/T07_Learner_Lab_Limitations.md) | Lab limitations | COMPLETED |

Ten findings are recorded in the [findings register](10_Audit_Findings/Findings_Register.csv). **Internet-wide SSH access** and **unencrypted EBS storage** are rated Major / High. **Cognito MFA not enforced** is rated Minor / Medium. The remaining seven observations address logging, S3, SNS, RDS and network hardening.

Prowler produced **467 check-resource results: 342 PASS, 111 FAIL and 14 MANUAL**. Failed rows are individually triaged and consolidated by root cause. ScoutSuite provides cross-tool support, with 31 collection-error records limiting coverage. Scanner execution success does not establish security compliance.

## Documentation

| Document | Purpose |
|---|---|
| [Audit checklist](03_Audit_Checklist/README.md) | Seven-test grid and detailed verification points |
| [Architecture](04_Architecture/README.md) | Application flows and deployment boundaries |
| [Setup](05_Setup/README.md) | Workstation, CLI and scanner procedures |
| [Configuration](06_Configuration/README.md) | Observed AWS baseline |
| [Evidence index](08_Evidence/README.md) | Evidence groups and interpretation limits |
| [Test results](09_Test_Results/README.md) | Execution summary |
| [Findings](10_Audit_Findings/README.md) | Ratings and scanner dispositions |
| [Corrective actions](12_Corrective_Action_Plan/README.md) | Priorities, proposed owners and closure criteria |
| [Evidence limitations](14_Appendices/Evidence_Gaps_and_Interpretation.md) | Missing primary sources and assurance boundaries |

Supporting AWS captures, scanner exports and session documents are organized in the evidence groups. The [evidence-handling policy](08_Evidence/Evidence_Handling.md) defines access and source interpretation. Remediation is planned and has not been verified.
