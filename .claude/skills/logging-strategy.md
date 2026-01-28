# Logging Strategy

## Rules
- Log to stdout/stderr, not files
- Use structured logging (JSON format)
- Include correlation IDs for request tracing
- Avoid logging sensitive data

## Analysis
This skill establishes cloud-native logging practices. Logging to stdout/stderr allows container orchestrators to collect logs without requiring volume mounts or sidecar containers, simplifying log aggregation. Structured JSON logging enables efficient parsing, filtering, and querying in log management systems. Correlation IDs link related log entries across services, essential for debugging distributed systems. Avoiding sensitive data in logs prevents credential leaks and supports compliance requirements, though care must be taken to balance debuggability with security.
