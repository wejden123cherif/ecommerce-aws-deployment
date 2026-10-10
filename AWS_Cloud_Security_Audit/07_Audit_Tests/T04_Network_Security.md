# T-04 — Network Security

**Test ID:** T-04  
**Audit criterion:** G-04 — documented project requirement mapped to A.8.9  
**ISO control:** ISO/IEC 27001:2022 A.8.9  
**Audit question:** Are network access rules appropriately restrictive?  
**Method:** Manual SG/VPC review and scanner correlation

## Resources examined

VPC vpc-082a310dcc24141fe; ALB SG sg-0464d411ab9505f1e; EC2 SG sg-045fb00f9aadc1d96; linked EC2/RDS SG pair and additional RDS SG; collected NACL/flow-log configuration.

## Evidence reference

Primary group: [EV-004](../08_Evidence/EV-004_Network_Security/README.md). Cross-tool support: [EV-006](../08_Evidence/EV-006_Security_Scan/README.md); environment qualifications: [EV-007](../08_Evidence/EV-007_Lab_Limitations/README.md). Documentary execution source: Session 2 (`../09_Test_Results/Session_2_Final_Audit_Execution.docx`; private source). File-level paths and hashes are in the evidence register and traceability matrix.

## Findings/observations

F-01 (Major / High), F-09 and F-10 (observations). TCP/5543 is a real additional rule; its need is unproven. SG configuration is not an exploit test. An ingress rule for 443 does not prove an HTTPS listener.

**Control:** A.8.9  
**Evidence:** EV-004  
**Result:** PARTIAL  
**Classification:** Major nonconformity

## Procedure executed
The team reviewed VPC/subnet placement, ALB and EC2 security groups, the EC2-to-RDS security-group path, additional RDS rules, NACL observations and scanner findings.

## Observed result
- ALB security group permits TCP/80 and TCP/443 from `0.0.0.0/0`.
- EC2 application ports 5000 and 5500 are restricted to the ALB security group.
- EC2 SSH TCP/22 is open from `0.0.0.0/0`.
- RDS PostgreSQL connectivity uses TCP/5432 through the linked EC2/RDS security-group pair.
- A separate RDS security group contains TCP/5543 from the EC2 security group; this is recorded as a potential stale/unused rule because the verified PostgreSQL port is 5432.
- ScoutSuite reports permissive default NACL behavior and subnets without flow logs.
- Prowler reports a VPC endpoint trust-boundary issue; because the endpoint policy was not independently validated, this remains a scanner observation and is not raised as a separate confirmed nonconformity.

## Conclusion
The public SSH rule is a significant network-security gap and is independently corroborated by Prowler and ScoutSuite. T-04 is a major nonconformity.
