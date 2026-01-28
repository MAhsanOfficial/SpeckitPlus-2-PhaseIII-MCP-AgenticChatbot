# Storage Management

## Rules
- Define StorageClasses for different performance tiers
- Use dynamic provisioning over static volumes
- Implement volume snapshots for backups
- Monitor storage capacity and performance

## Analysis
This skill ensures proper persistent storage management in Kubernetes. StorageClasses define different storage tiers (SSD, HDD, network storage) with appropriate performance characteristics and costs. Dynamic provisioning automatically creates volumes on demand, simplifying operations compared to pre-creating static volumes. Volume snapshots provide point-in-time backups and enable cloning for testing or disaster recovery. Monitoring storage capacity prevents out-of-space errors, while performance monitoring identifies I/O bottlenecks, though storage costs can escalate quickly without proper governance.
