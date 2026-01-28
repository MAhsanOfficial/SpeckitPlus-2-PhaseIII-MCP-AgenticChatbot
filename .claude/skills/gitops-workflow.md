# GitOps Workflow

## Rules
- Git is the single source of truth
- Declarative infrastructure definitions
- Automated sync from repository
- Audit trail through commit history

## Analysis
This skill establishes GitOps as the deployment methodology for infrastructure and applications. Using Git as the single source of truth ensures that the desired state is version-controlled, reviewable, and recoverable. Declarative definitions (YAML manifests, Helm charts) describe what should exist rather than how to create it, enabling idempotent operations. Automated synchronization tools continuously reconcile the cluster state with the Git repository, reducing manual intervention and configuration drift. The commit history provides a complete audit trail of all changes, supporting compliance requirements and simplifying rollbacks to known-good states.
