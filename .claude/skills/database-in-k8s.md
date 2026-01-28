# Database in Kubernetes

## Rules
- Use StatefulSets for stateful workloads
- Implement persistent volume claims
- Configure backup strategies before production
- Separate database credentials per environment

## Analysis
This skill addresses the unique challenges of running databases in Kubernetes. StatefulSets provide stable network identities and ordered deployment/scaling, essential for database clusters. Persistent Volume Claims ensure data survives pod restarts and rescheduling. Backup strategies must be established early, including automated backups, point-in-time recovery capabilities, and tested restore procedures. Environment-specific credentials prevent accidental production data access from non-production environments and support the principle of least privilege across the deployment pipeline.
