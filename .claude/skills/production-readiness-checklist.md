# Production Readiness Checklist

## Rules
- Implement health checks (liveness and readiness)
- Define resource requests and limits
- Configure proper logging and monitoring
- Set up backup and disaster recovery

## Analysis
This skill ensures applications are production-ready before deployment. Health checks enable Kubernetes to manage pod lifecycle automatically, restarting failed containers and routing traffic only to ready instances. Resource requests and limits prevent resource starvation and enable proper scheduling. Logging and monitoring provide visibility into application behavior and performance. Backup and disaster recovery procedures protect against data loss and enable business continuity. Production readiness is a gate that prevents immature applications from reaching users, though the specific requirements vary by application criticality and organizational standards.
