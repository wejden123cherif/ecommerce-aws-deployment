# Project Scope — AWS Cloud Security Audit

## 1. Project Identification

**Project title:** Audit of the Security of a Cloud Environment  
**Environment:** AWS Academy Learner Lab  
**AWS Account:** 623463264556  
**Primary Region:** us-east-1 (US East — N. Virginia)  
**Audit type:** Cloud configuration security audit  
**Application context:** E-commerce cloud environment  
**Audit team:** Wejden Cherif and Maram Raboudi  
**Professor:** Mohamed Ali Hadhri  
**Reference framework:** ISO/IEC 27001:2022 controls A.5.23, A.5.15 and A.8.9  

The Terms of Reference defines the assignment as an audit of a cloud environment focused on identities, storage and network configuration, with additional verification of logging and automated security scanning. The mandatory controls are A.5.23, A.5.15 and A.8.9.

---

## 2. Purpose of the Audit

The purpose of this audit is to evaluate the security configuration of the AWS environment supporting the e-commerce application and determine whether the implemented controls provide adequate protection for:

- cloud-service governance and responsibilities;
- identity and access control;
- authentication;
- storage confidentiality and encryption;
- network segmentation and access restrictions;
- logging and monitoring;
- security configuration management;
- automated security assessment;
- limitations imposed by the AWS Academy Learner Lab environment.

The audit is evidence-based. Every conclusion must be supported through the following traceability chain:

**CRITERION → CONTROL → TEST → EVIDENCE → RESULT → FINDING**

---

## 3. Audit Environment

The audit was performed on the real AWS Academy Learner Lab environment used for the e-commerce project.

The final audit target consists of real AWS resources in the AWS Academy Learner Lab.

The audited environment is hosted in:

- **AWS Account:** 623463264556
- **AWS Region:** us-east-1
- **Primary VPC:** vpc-082a310dcc24141fe

Administrative access to the AWS environment is provided through temporary AWS STS credentials and an AWS Academy/Vocareum-managed assumed role.

The audit team therefore does not have the same administrative capabilities as the owner of a normal unrestricted AWS account. Restrictions imposed by AWS Academy/Vocareum are recorded under **T-07 / EV-007 — Lab Environment Limitations**.

---

## 4. Functional Scope

The audit covers the following security areas:

### 4.1 Cloud Governance

The audit verifies whether responsibilities for use and administration of the cloud environment are identified and documented.

Associated control:

**A.5.23 — Information security for use of cloud services**

Associated test:

**T-01 — Cloud usage policy and responsibilities**

Evidence:

**EV-001**

---

### 4.2 Identity and Access Management

The audit evaluates:

- AWS administrative access through the Learner Lab assumed-role model;
- IAM roles and policies visible to the audit team;
- excessive privileges detected by automated scanners;
- Amazon Cognito user authentication;
- Cognito group-based authorization;
- MFA configuration;
- access restrictions imposed by the Learner Lab.

Associated control:

**A.5.15 — Access control**

Associated test:

**T-02 — Identities and access**

Evidence:

**EV-002**

---

### 4.3 Storage Security

The audit evaluates security controls protecting stored data, including:

- Amazon RDS storage encryption;
- private placement of the RDS database;
- RDS credentials stored in AWS Secrets Manager;
- Amazon S3 storage used by CloudTrail;
- S3 Block Public Access;
- S3 server-side encryption;
- EC2/EBS storage configuration identified by automated scanning;
- relevant backup and recovery configuration.

Associated control:

**A.8.9 — Configuration management**

Associated test:

**T-03 — Storage security**

Evidence:

**EV-003**

---

### 4.4 Network Security

The audit evaluates:

- VPC configuration;
- public and private subnet separation;
- security groups;
- EC2 inbound access;
- ALB inbound access;
- EC2-to-RDS communication;
- RDS database access;
- Network ACL configuration;
- VPC endpoints where relevant;
- exposure of administrative services to the Internet.

The audit specifically verifies whether sensitive ports are exposed through rules such as `0.0.0.0/0`.

Associated control:

**A.8.9 — Configuration management**

Associated test:

**T-04 — Network security**

Evidence:

**EV-004**

---

### 4.5 Logging, Monitoring and Alerting

The audit evaluates:

- AWS CloudTrail;
- CloudTrail S3 log delivery;
- CloudWatch log groups;
- EC2 metrics;
- Application Load Balancer metrics;
- RDS log publication;
- CloudWatch alarms;
- SNS security notifications;
- log retention configuration;
- CloudTrail integrity and hardening settings.

Associated control:

**A.8.9 — Configuration management**

Associated test:

**T-05 — Logging and monitoring**

Evidence:

**EV-005**

---

### 4.6 Automated Security Assessment

Two automated AWS configuration assessment tools were used:

#### Prowler

Prowler 5.44.0 was executed against AWS account 623463264556.

The final scan produced:

- 467 resource/check results;
- 342 passed results;
- 111 failed results;
- 14 MANUAL results;
- HTML report;
- CSV report;
- OCSF JSON report.

Critical and High results were extracted separately for manual analysis and correlation with the evidence collected during the audit.

#### ScoutSuite

ScoutSuite was also executed against the same AWS Learner Lab environment.

The generated evidence includes:

- HTML security report;
- ScoutSuite result data;
- collection/error report;
- browser-based findings dashboard.

The use of both tools provides additional corroboration of manually identified configuration issues.

Associated control:

**A.8.9 — Configuration management**

Associated test:

**T-06 — Scanner execution**

Evidence:

**EV-006**

---

### 4.7 Laboratory Environment Limitations

The audit explicitly documents restrictions and behaviours caused by AWS Academy/Vocareum.

Observed limitations include:

- AWS access through temporary STS assumed-role credentials;
- restrictions on IAM administrative operations;
- AccessDenied when attempting some IAM changes;
- inability to attach the IAM policy required for the intended CloudTrail-to-CloudWatch Logs configuration;
- restricted access to some AWS configuration information;
- inability to create IAM users;
- scanner results that may be affected by insufficient permissions;
- temporary Learner Lab sessions;
- AWS provider capacity limitations encountered when starting the RDS instance;
- platform-managed EC2 behaviour observed through CloudTrail;
- local WSL/tooling limitations encountered during scanner installation.

These conditions are treated separately from security misconfigurations created by the e-commerce project.

Associated control:

**A.8.9 — Configuration management**

Associated test:

**T-07 — Lab environment limitations**

Evidence:

**EV-007**

---

## 5. Technical Scope

The following AWS resources and services form part of the audit scope.

| Category | Audited resource / service |
|---|---|
| AWS Account | 623463264556 |
| Region | us-east-1 |
| VPC | vpc-082a310dcc24141fe |
| Compute | EC2 instance i-03687e15b74af60a4 |
| EC2 Storage | EBS storage associated with the audited instance |
| Load Balancing | Application Load Balancer (ALB) |
| Database | Amazon RDS PostgreSQL — database-1 |
| Identity | IAM / STS assumed roles |
| Application Authentication | Amazon Cognito |
| Secrets | AWS Secrets Manager |
| Object Storage | Amazon S3 |
| Network Security | Security Groups and Network ACLs |
| Private Connectivity | VPC endpoint configuration |
| Audit Logging | AWS CloudTrail |
| Monitoring | Amazon CloudWatch |
| Alerting | Amazon SNS |
| Encryption | AWS KMS-related configuration |
| Web Security | AWS WAF |
| Automated Audit | Prowler and ScoutSuite |

---

## 6. Application Architecture in Scope

The audited application follows the general communication path:

**Public User → Cloudflare → AWS WAF → Application Load Balancer → EC2 → Amazon RDS PostgreSQL**

The EC2 instance hosts the e-commerce application services.

The Application Load Balancer distributes incoming application traffic toward the EC2-hosted services.

Amazon Cognito provides application-user authentication.

The RDS PostgreSQL database is located in private database subnets and is accessed from the application environment through controlled security-group rules.

AWS CloudTrail, CloudWatch and SNS provide audit logging, infrastructure monitoring and security notification capabilities.

Cloudflare is represented as architectural context but its internal configuration is not part of the AWS configuration audit.

---

## 7. Audit Criteria and Tests

| Test | Control | Audit Question | Evidence |
|---|---|---|---|
| T-01 | A.5.23 | Are cloud responsibilities defined? | EV-001 |
| T-02 | A.5.15 | Are access rights limited and strong authentication controls implemented? | EV-002 |
| T-03 | A.8.9 | Is storage protected from public exposure and appropriately encrypted? | EV-003 |
| T-04 | A.8.9 | Are network access rules appropriately restrictive? | EV-004 |
| T-05 | A.8.9 | Are logging, monitoring and alerting controls operational? | EV-005 |
| T-06 | A.8.9 | Can automated security scanners execute and produce usable reports? | EV-006 |
| T-07 | A.8.9 | Are AWS Academy Learner Lab limitations identified and documented? | EV-007 |

---

## 8. Evidence Scope

Audit evidence is organised using identifiers EV-001 through EV-007.

Evidence includes:

- AWS console screenshots;
- AWS configuration details;
- CloudTrail events;
- CloudWatch monitoring evidence;
- security-group rules;
- IAM/Cognito configuration;
- S3 and RDS configuration;
- Prowler reports;
- ScoutSuite reports;
- scanner result extracts;
- AccessDenied messages;
- Learner Lab limitation screenshots;
- evidence hashes and evidence-register entries.

The evidence is stored under:

`08_Evidence/`

with a dedicated directory for each EV identifier.

---

## 9. Out of Scope

The following activities and systems are outside the scope of this audit:

- penetration testing against production or third-party systems;
- exploitation of identified vulnerabilities;
- denial-of-service testing;
- destructive testing;
- application source-code security review;
- malware deployment;
- Cloudflare internal infrastructure;
- AWS physical infrastructure;
- AWS-managed infrastructure that is not configurable by the audit team;
- other AWS accounts;
- AWS regions not involved in the audited architecture;
- resources clearly unrelated to the e-commerce application, except where they affect account-level security posture;
- remediation of findings during evidence collection.

Scanner findings concerning unrelated laboratory resources such as EKS, EMR or Redshift components are not automatically classified as e-commerce application findings. Their applicability must first be established.

---

## 10. Audit Boundaries

This audit evaluates the configuration observed during the defined audit period.

A scanner failure does not automatically represent an independent vulnerability. Automated findings are correlated with manual evidence before they are included in the final findings register.

Multiple scanner checks identifying the same underlying configuration weakness are consolidated into a single audit finding where appropriate.

AWS Academy/Vocareum-managed configuration is distinguished from configuration controlled by the e-commerce project team.

The assessment represents a point-in-time evaluation and does not constitute permanent certification of the AWS environment.

---

## 11. Scope Conclusion

The defined scope covers the AWS resources and security controls necessary to answer all seven audit questions required by the Terms of Reference.

The audit therefore evaluates:

**governance → identity → storage → network → logging → automated assessment → laboratory limitations**

within the real AWS Academy Learner Lab environment hosting the e-commerce project.

The scope is sufficiently bounded to produce reproducible evidence while excluding destructive testing, unrelated external infrastructure and resources outside the audit team's authorised control.