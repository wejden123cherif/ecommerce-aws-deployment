# Setup Validation Checklist

| Check | Status | Evidence / note |
|---|---|---|
| Ubuntu/WSL workstation available | PASS | Ubuntu 24.04.4 LTS |
| Python available | PASS | Python 3.12 |
| AWS CLI installed | PASS | Used successfully with Learner Lab |
| AWS account identity validated | PASS | Account `623463264556` |
| Target region established | PASS | `us-east-1` |
| Prowler isolated virtual environment | PASS | `~/prowler-venv` |
| Prowler installation validated | PASS | Version 5.44.0 |
| Prowler report generated | PASS | HTML / CSV / OCSF JSON |
| ScoutSuite isolated virtual environment | PASS | `~/scoutsuite-venv` |
| ScoutSuite report generated | PASS | HTML / JS result data / error data |
| Temporary credential handling documented | PASS | Setup instructions contain no credential literals; raw exports require controlled handling |
| Local tooling limitations documented | PASS | WSL read-only filesystem incident recorded |

## Conclusion

The audit tooling environment was successfully installed and validated. Both automated scanners executed against the intended AWS Learner Lab account and generated usable evidence for T-06.
