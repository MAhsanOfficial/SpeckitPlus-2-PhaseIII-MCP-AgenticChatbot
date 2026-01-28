# Container Security

## Rules
- Run containers as non-root user
- Use minimal base images (distroless/alpine)
- Scan images for vulnerabilities
- Implement read-only root filesystems where possible

## Analysis
This skill enforces container security hardening practices. Running as non-root reduces the attack surface by limiting privileges if a container is compromised. Minimal base images reduce the number of potential vulnerabilities and decrease image size, improving pull times and security posture. Regular vulnerability scanning identifies known CVEs before deployment. Read-only root filesystems prevent runtime modifications, making it harder for attackers to persist malware or modify application code, though temporary directories must be mounted as volumes for applications requiring write access.
