# EV-004 — Network Security

**Evidence ID:** EV-004\
**Related test:** T-04 / G-04\
**ISO control:** ISO/IEC 27001:2022 A.8.9

## What the evidence supports

Reviewed security groups and VPC map, including public TCP/22, ALB-restricted application ports and the linked TCP/5432 database path.

## Supporting artifacts

Console captures and raw scanner exports are held privately.

- `EV004-01_Security_Groups_Inventory.png`
- `EV004-02_EC2_SG_Inbound_Rules_Overview.png`
- `EV004-03_ALB_SG_Inbound_Rules_Overview.png`
- `EV004-04_RDS_SG_TCP5543_Overview.png`
- `EV004-05_RDS_SG_TCP5543_Source_EC2.png`
- `EV004-06_EC2_SG_SSH_0.0.0.0_0_and_App_Ports.png`
- `EV004-07_ALB_SG_HTTP_HTTPS_0.0.0.0_0.png`
- `EV004-08_RDS_EC2_Linked_SG_PostgreSQL_5432.png`
- `EV004-09_EC2_RDS_Linked_SG_No_Inbound.png`
- `EV004-10_VPC_Resource_Map_Private_RDS_Subnets.png`

## Interpretation limits

TCP/5543 is a real additional rule; its need is unproven. SG configuration is not an exploit test. An ingress rule for 443 does not prove an HTTPS listener.

See [evidence handling](../Evidence_Handling.md) for source provenance and access to supporting artifacts.
