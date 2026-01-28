# Cluster Maintenance

## Rules
- Schedule regular cluster upgrades
- Drain nodes before maintenance
- Test upgrades in non-production first
- Maintain cluster component version compatibility

## Analysis
This skill ensures reliable cluster operations through proper maintenance practices. Regular upgrades provide security patches, bug fixes, and new features, though they require planning to avoid disruption. Draining nodes gracefully evicts pods before maintenance, preventing service interruption. Testing upgrades in non-production catches compatibility issues before they affect users. Maintaining version compatibility between cluster components (kubelet, kube-proxy, API server) prevents subtle bugs and ensures supported configurations, though version skew policies must be understood and followed.
