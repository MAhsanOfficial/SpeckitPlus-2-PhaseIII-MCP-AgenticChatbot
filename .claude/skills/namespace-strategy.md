# Namespace Strategy

## Rules
- Use namespaces for logical isolation
- Implement resource quotas per namespace
- Apply network policies at namespace boundaries
- Establish naming conventions

## Analysis
This skill establishes effective namespace organization in Kubernetes. Namespaces provide logical isolation between teams, environments, or applications, preventing naming conflicts and enabling scoped access control. Resource quotas per namespace prevent resource hogging and enable cost allocation. Network policies at namespace boundaries implement defense in depth, restricting cross-namespace communication to explicitly allowed paths. Naming conventions (e.g., team-app-env) improve clarity and support automation, though excessive namespaces can complicate cluster management.
