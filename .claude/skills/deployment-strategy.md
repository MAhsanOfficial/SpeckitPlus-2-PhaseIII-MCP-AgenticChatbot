# Deployment Strategy

## Rules
- Use rolling updates as default
- Define maxUnavailable and maxSurge
- Implement readiness probes before traffic routing
- Plan rollback procedures

## Analysis
This skill ensures zero-downtime deployments through proper update strategies. Rolling updates gradually replace old pods with new ones, maintaining service availability. MaxUnavailable and maxSurge parameters control the update pace, balancing deployment speed with resource usage and availability requirements. Readiness probes prevent routing traffic to pods that aren't ready to serve requests, avoiding user-facing errors during deployments. Pre-planned rollback procedures enable quick recovery from problematic releases, with Kubernetes supporting instant rollback to previous ReplicaSet configurations.
