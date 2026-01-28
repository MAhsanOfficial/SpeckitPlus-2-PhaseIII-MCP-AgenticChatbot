# Configuration Management

## Rules
- Use ConfigMaps for non-sensitive config
- Use Secrets for sensitive data
- Mount configs as volumes, not environment variables (when possible)
- Version configuration alongside code

## Analysis
This skill establishes proper configuration management in Kubernetes. ConfigMaps separate configuration from container images, enabling the same image to run with different configs across environments. Secrets provide base64 encoding and access controls for sensitive data, though external secret managers offer stronger security. Mounting configs as volumes allows dynamic updates without pod restarts, though environment variables are simpler for static configs. Versioning configuration alongside code in Git ensures configuration changes are tracked, reviewed, and can be rolled back, supporting GitOps workflows and audit requirements.
