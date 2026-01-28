# Zero-Downtime Deployment

## Rules
- Use rolling updates as default strategy
- Implement readiness probes correctly
- Set appropriate terminationGracePeriodSeconds
- Test deployment process in staging

## Analysis
This skill ensures deployments don't impact user experience. Rolling updates gradually replace old pods with new ones, maintaining service availability throughout. Correct readiness probes prevent traffic routing to pods that aren't ready, avoiding user-facing errors. Appropriate grace periods allow pods to finish in-flight requests before termination. Testing in staging validates the deployment process and catches configuration issues before production. Zero-downtime deployments are critical for user-facing services and require careful coordination between application code (graceful shutdown) and infrastructure configuration (health checks, update strategy).
