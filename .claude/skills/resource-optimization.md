# Resource Optimization

## Rules
- Right-size resource requests based on metrics
- Use Horizontal Pod Autoscaling (HPA)
- Implement Pod Disruption Budgets (PDB)
- Monitor and optimize container startup time

## Analysis
This skill ensures efficient resource utilization in Kubernetes clusters. Right-sizing resource requests prevents over-provisioning waste and under-provisioning performance issues, requiring metrics-driven analysis of actual usage patterns. HPA automatically scales pods based on CPU, memory, or custom metrics, handling traffic spikes without manual intervention. Pod Disruption Budgets ensure minimum availability during voluntary disruptions like node drains or cluster upgrades. Optimizing startup time reduces scaling latency and improves deployment speed, achieved through image optimization, dependency caching, and lazy initialization patterns.
