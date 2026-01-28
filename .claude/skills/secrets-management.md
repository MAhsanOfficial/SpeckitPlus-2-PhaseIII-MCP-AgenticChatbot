# Secrets Management

## Rules
- Never commit secrets to version control
- Use Kubernetes Secrets with RBAC
- Rotate secrets regularly
- Consider external secret managers (Vault, AWS Secrets Manager)

## Analysis
This skill enforces secure secret handling in Kubernetes environments. Excluding secrets from version control prevents credential leaks and supports security audits. Kubernetes Secrets with RBAC provide basic secret storage with access controls, though they're base64-encoded rather than encrypted at rest by default. Regular rotation limits the window of exposure if secrets are compromised. External secret managers offer stronger encryption, audit logging, and centralized management across multiple clusters, though they add operational complexity and external dependencies.
