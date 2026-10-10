# T-06 — Automated Security Scanning

**Test ID:** T-06  
**Audit criterion:** G-06 — documented project requirement mapped to A.8.9  
**ISO control:** ISO/IEC 27001:2022 A.8.9  
**Audit question:** Did both automated scanners execute and produce usable reports?  
**Method:** Historical scan execution review; raw-output parsing and dashboard inspection

## Resources examined

Account 623463264556 / us-east-1; Prowler 5.44.0 final run; earlier Prowler run; ScoutSuite 5.14.0 report and collection errors.

## Evidence reference

Primary group: [EV-006](../08_Evidence/EV-006_Security_Scan/README.md). Cross-tool support: [EV-006](../08_Evidence/EV-006_Security_Scan/README.md); environment qualifications: [EV-007](../08_Evidence/EV-007_Lab_Limitations/README.md). Documentary execution source: Session 2 (`../09_Test_Results/Session_2_Final_Audit_Execution.docx`; private source). File-level paths and hashes are in the evidence register and traceability matrix.

## Findings/observations

No independent finding for successful execution; results corroborate T-02 through T-05. Successful scanning does not imply a secure environment. Failed check-resource rows require scope/ownership triage; collection errors and MANUAL rows limit assurance.

**Control:** A.8.9  
**Evidence:** EV-006  
**Result:** PASS  
**Classification:** Compliant

## Procedure executed

Reviewed both documented scanner runs, analyzed the Prowler CSV and ScoutSuite result data, and inspected the eight ScoutSuite dashboards. The results describe the recorded audit runs.

## Observed result

### Prowler
Prowler 5.44.0 successfully authenticated to AWS account `623463264556` and scanned the selected AWS services in `us-east-1`.

Final overview:
- 467 resource/check results
- 342 passed
- 111 failed
- 14 MANUAL results
- 0 muted

Prowler generated HTML, semicolon-delimited CSV and OCSF JSON reports. Critical/High results were extracted and manually triaged. Duplicate checks against the same root cause were consolidated rather than counted as separate audit findings.

### ScoutSuite
ScoutSuite successfully produced an offline HTML report and supporting result/error files. Dashboard evidence was captured for the overall account and relevant services including CloudTrail, CloudWatch, EC2, KMS, RDS, IAM and VPC.

ScoutSuite independently corroborated key issues including:
- EC2 SSH exposure;
- unencrypted EBS storage;
- EBS encryption-by-default disabled;
- CloudTrail hardening gaps;
- RDS resilience/backup observations;
- permissive default network controls.

## Conclusion
Both required automated configuration-audit tools executed successfully and produced usable evidence. T-06 is compliant.
