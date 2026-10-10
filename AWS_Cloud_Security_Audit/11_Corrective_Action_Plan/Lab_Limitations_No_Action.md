# Learner Lab Limitations — No Direct Corrective Action by Student Team

The following items are documented but are not assigned normal corrective actions because they are controlled by AWS Academy/Vocareum or the provider environment:

1. Temporary STS assumed-role access under the Vocareum Learner Lab.
2. `iam:CreateUser` denied.
3. `iam:AttachRolePolicy` denied during CloudTrail-to-CloudWatch Logs integration.
4. CloudTrail console AccessDenied for selected resources/actions.
5. Prowler checks that are explicitly inconclusive because the `voclabs` role cannot read a resource policy.
6. Provider capacity error when starting the RDS `db.t4g.micro` instance in `us-east-1a`.
7. Vocareum-managed EC2 `StartInstances` activity observed in CloudTrail.
8. Local WSL filesystem/I/O instability encountered during the first scanner installation attempt.

Items 6–8 are retained secondary Session 2 narratives; their original capacity-error, CloudTrail-event and WSL artifacts are absent. Temporary-session expiry is a documented constraint of the access model, without a retained direct AWS expiry capture.

For these items, the appropriate treatment is documentation, evidence preservation, and escalation to the lab/provider/teacher when they prevent completion of an intended security control. They must not be misclassified as application-team configuration failures.
