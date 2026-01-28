# Cloud-Native Discipline

## Rules
- Stateless containers
- Config via env vars
- No hardcoded secrets

## Analysis
This skill enforces cloud-native best practices for containerized applications. Stateless containers ensure that any instance can be terminated and replaced without data loss, enabling seamless scaling and rolling updates. Configuration via environment variables follows the twelve-factor app methodology, allowing the same container image to run in different environments (dev, staging, production) without rebuilding. Eliminating hardcoded secrets prevents credential leaks in version control and container registries, while enabling secure secret injection through Kubernetes Secrets or external secret management systems at runtime.
