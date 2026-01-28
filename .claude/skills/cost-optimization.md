# Cost Optimization

## Rules
- Use resource quotas per namespace
- Implement cluster autoscaling
- Schedule non-critical workloads on spot instances
- Monitor and eliminate idle resources

## Analysis
This skill ensures efficient cloud spending in Kubernetes environments. Resource quotas prevent runaway resource consumption and enable cost allocation by team or project. Cluster autoscaling adjusts node count based on demand, avoiding over-provisioning during low traffic periods. Spot instances offer significant cost savings for fault-tolerant workloads like batch jobs or stateless services. Monitoring idle resources (unused PVCs, over-provisioned pods, orphaned load balancers) and eliminating them prevents waste, though it requires regular audits and automation.
