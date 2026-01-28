# Pod Security Standards

## Rules
- Enforce restricted pod security standard
- Prohibit privileged containers
- Require non-root users
- Drop unnecessary capabilities

## Analysis
This skill hardens pod security through Kubernetes Pod Security Standards. The restricted standard enforces security best practices, preventing common misconfigurations. Prohibiting privileged containers limits access to host resources, containing potential breaches. Requiring non-root users reduces the impact of container escapes and follows least privilege principles. Dropping unnecessary Linux capabilities (like NET_ADMIN, SYS_ADMIN) minimizes the attack surface, though some applications may require specific capabilities that must be explicitly granted and justified.
