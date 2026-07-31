# Security Policy: eventhub-otlp-mapper

## Supported Versions

| Version | Supported |
|---|---|
| 1.1.x | Yes |
| < 1.1 | No |

## Reporting a Vulnerability

Open a GitHub issue with the label `security`. Describe the vulnerability type and the affected component.
Do not include exploit code in public issues.

I aim to respond within 72 hours and provide a fix within 14 days for confirmed vulnerabilities.

## Credential Handling

This tool reads credentials exclusively from environment variables (see `.env.example`).
Never commit `.env` files or connection strings to version control.
All secrets must be managed via your CI/CD secret store or Azure Key Vault.
