# Prowler assessment

**Version:** 5.44.0\
**Region:** `us-east-1`\
**Final run:** `20261009203250`

The final CSV records `2026-10-09 20:32:50.556875` without an explicit timezone. The earlier run is `20261009202255`; its execution capture supports tool execution, while the final completion capture identifies the final output files.

HTML, semicolon-delimited CSV and OCSF JSON exports support the assessment. The final run contains **467 check-resource rows: 342 PASS, 111 FAIL and 14 MANUAL**. The completion capture reports 280 checks and zero muted results. A Critical/High extraction contains 28 failed rows: 2 Critical and 26 High.

The [disposition analysis](Analysis/README.md) accounts for all 111 failed rows. These are scanner observations requiring interpretation; they do not represent 111 independent vulnerabilities. Raw reports and captures are held in the private evidence record.
