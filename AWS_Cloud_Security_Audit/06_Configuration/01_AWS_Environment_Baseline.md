# AWS Environment Baseline

## 1. Account and region

```text
AWS Account: 623463264556
Primary Region: us-east-1
Environment: AWS Academy Learner Lab
```

Administrative access is supplied by AWS Academy/Vocareum through temporary STS assumed-role credentials.

## 2. Application architecture

The observed application path is:

```text
Public user
  → Cloudflare DNS / Worker reverse proxy
  → AWS WAF
  → AWS Application Load Balancer
  → EC2 Docker Compose application host
  → Amazon RDS PostgreSQL
```

Cloudflare provides the public-facing TLS certificate. The Worker contains reverse-proxy logic that maps and forwards requests toward the AWS ALB. The verified ALB listener is HTTP port 80, therefore the Cloudflare certificate alone does not prove encryption on the Cloudflare-to-ALB origin hop.

## 3. VPC baseline

Primary application VPC:

```text
vpc-082a310dcc24141fe
```

A second VPC was also present:

```text
vpc-076fe7171cef3d8db
```

The primary VPC resource map showed nine subnets and five route tables. Public application subnets and private RDS subnets are present. The RDS private route table was observed with local-only routing in the relevant view.

## 4. Compute

Main EC2 instance:

```text
i-03687e15b74af60a4
```

The instance is deployed in a public subnet and hosts the Docker Compose e-commerce services, including frontend, API gateway and application microservices.

## 5. Load balancer

Application Load Balancer:

```text
Name: ALB
DNS: ALB-1851337185.us-east-1.elb.amazonaws.com
Verified listener: HTTP / TCP 80
```

Observed listener routing:

- priority 10: `/users*`, `/products*`, `/orders*` → API Gateway target group
- default rule → frontend target group

## 6. Database

```text
Identifier: database-1
Engine: PostgreSQL 18.3
Class: db.t4g.micro
AZ: us-east-1a
Port: 5432
Storage: 20 GiB gp2
Storage autoscaling: enabled
Maximum storage threshold: 1000 GiB
Storage encryption: enabled
KMS key: aws/rds
Master credentials: AWS Secrets Manager
IAM DB authentication: disabled
Deletion protection: disabled
Multi-AZ: No
```

The database is associated with the private database subnet structure and with the linked EC2-to-RDS security group pair described in the network configuration file.
