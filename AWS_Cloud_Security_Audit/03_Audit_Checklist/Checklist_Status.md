# Audit checklist status

All seven planned tests have a final execution status and evidence reference.

- T-01: assessed — compliant.
- T-02: assessed — minor nonconformity for application MFA, with Learner Lab IAM context separated.
- T-03: assessed — major nonconformity for unencrypted EC2 EBS storage; RDS and the audited CloudTrail S3 bucket remain protected.
- T-04: assessed — major nonconformity for Internet-exposed SSH; application and database rules otherwise show useful segmentation, with additional observations recorded.
- T-05: assessed — logging/monitoring operational with hardening observations and one lab-permission limitation.
- T-06: assessed — Prowler and ScoutSuite both executed and produced usable reports.
- T-07: assessed — Learner Lab limitations documented, with primary and secondary sources distinguished.

All checklist rows have a recorded result. Scanner-only observations that could not be independently confirmed have a documented final disposition and are not presented as confirmed application vulnerabilities.
