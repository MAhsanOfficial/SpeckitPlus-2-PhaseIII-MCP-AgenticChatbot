# Custom Resources and Operators

## Rules
- Use CRDs for domain-specific abstractions
- Implement operators for complex lifecycle management
- Follow operator best practices (idempotency, status updates)
- Version CRDs properly for backward compatibility

## Analysis
This skill guides the creation of Kubernetes extensions through Custom Resource Definitions and Operators. CRDs extend Kubernetes with domain-specific resources (like Database, Certificate), providing declarative APIs for complex systems. Operators automate operational knowledge, handling installation, upgrades, backups, and failure recovery. Idempotent reconciliation ensures operators can safely retry operations, while status updates provide visibility into resource state. Proper CRD versioning enables schema evolution without breaking existing resources, though operators add significant development and maintenance complexity.
