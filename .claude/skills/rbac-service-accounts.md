# RBAC and Service Accounts

## Rules
- Follow principle of least privilege
- Create service accounts per application
- Use RoleBindings for namespace-scoped access
- Use ClusterRoleBindings sparingly

## Analysis
This skill enforces proper access control in Kubernetes clusters. Least privilege limits permissions to only what's necessary, reducing the impact of compromised credentials. Per-application service accounts enable fine-grained access control and audit trails. RoleBindings grant permissions within specific namespaces, containing the blast radius of compromised accounts. ClusterRoleBindings grant cluster-wide permissions and should be reserved for cluster-level operations like monitoring or operators, as they pose higher security risks if compromised.
