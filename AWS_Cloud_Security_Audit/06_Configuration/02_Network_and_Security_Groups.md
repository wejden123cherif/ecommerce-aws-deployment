# Network and Security Group Configuration

## 1. Primary VPC

```text
vpc-082a310dcc24141fe
```

The audited application uses public application subnets and private RDS subnets.

## 2. Observed security groups

Eight security groups were inventoried across the two VPCs. The most relevant groups are listed below.

| Group | ID | Observed purpose |
|---|---|---|
| Alb-sg | `sg-0464d411ab9505f1e` | Application Load Balancer |
| EC2 sg | `sg-045fb00f9aadc1d96` | Application EC2 instance |
| ec2-rds-1 | `sg-02b9c3fe59b6761ae` | EC2 side of AWS-created EC2↔RDS connection |
| rds-ec2-1 | `sg-089d2906b529750a6` | RDS side of EC2↔RDS connection |
| RDS sg | `sg-0069bef5caafbe7e9` | Additional RDS-related group |

## 3. ALB security group

`sg-0464d411ab9505f1e`:

| Protocol | Port | Source |
|---|---:|---|
| TCP | 80 | `0.0.0.0/0` |
| TCP | 443 | `0.0.0.0/0` |

The presence of a 443 security-group rule does not prove that an HTTPS listener is configured. The verified ALB listener is HTTP port 80.

## 4. EC2 security group

`sg-045fb00f9aadc1d96`:

| Protocol | Port | Source |
|---|---:|---|
| TCP | 22 | `0.0.0.0/0` |
| TCP | 5000 | `sg-0464d411ab9505f1e` (ALB SG) |
| TCP | 5500 | `sg-0464d411ab9505f1e` (ALB SG) |

The public SSH rule is the confirmed root cause of the main T-04 network finding and was corroborated by both manual review and automated scanning.

## 5. RDS linked security groups

RDS-side connection group `sg-089d2906b529750a6`:

```text
TCP 5432 from sg-02b9c3fe59b6761ae (ec2-rds-1)
```

EC2-side connection group `sg-02b9c3fe59b6761ae` had no inbound rules and one outbound rule in the observed configuration.

This is the verified PostgreSQL connectivity path.

## 6. Additional RDS security group

`sg-0069bef5caafbe7e9` contained:

```text
TCP 5543 from sg-045fb00f9aadc1d96 (EC2 sg)
```

The RDS engine itself is configured on TCP 5432. Therefore TCP 5543 is not treated as the PostgreSQL service port. It is documented as a potentially stale or unused rule whose operational purpose is not established by the retained evidence.

## 7. Network ACL observations

Prowler and ScoutSuite reported permissive/default Network ACL observations. These are retained as scanner observations and must be interpreted with the security-group controls rather than being treated as proof that all application ports are externally reachable.
