# Pod Scheduling Control

## Rules
- Use node affinity for hardware requirements
- Use pod affinity for co-location
- Use anti-affinity for high availability
- Implement taints and tolerations for dedicated nodes

## Analysis
This skill enables precise control over pod placement in Kubernetes clusters. Node affinity schedules pods on nodes with specific characteristics (GPU, SSD, region), ensuring workloads run on appropriate hardware. Pod affinity co-locates related pods to reduce latency or share volumes. Anti-affinity spreads pods across nodes or zones, improving availability during node failures. Taints and tolerations reserve nodes for specific workloads (like databases or batch jobs), preventing resource contention with general workloads, though complex scheduling rules can make troubleshooting difficult.
