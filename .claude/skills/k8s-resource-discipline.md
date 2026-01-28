# Kubernetes Resource Discipline

## Rules
- Always define resource requests and limits
- Use namespaces for isolation
- Apply labels and selectors consistently
- Never use 'latest' tag in production

## Analysis
This skill enforces Kubernetes resource management best practices. Resource requests and limits prevent resource starvation and enable proper scheduling, ensuring predictable application performance. Namespaces provide logical isolation between environments and teams, preventing accidental cross-contamination. Consistent labeling enables effective resource selection, monitoring, and management through kubectl and automation tools. Avoiding 'latest' tags ensures deployment reproducibility and prevents unexpected behavior from image updates, supporting reliable rollbacks and version tracking.
