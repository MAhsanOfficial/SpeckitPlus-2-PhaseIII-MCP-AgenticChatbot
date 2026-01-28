# Immutable Infrastructure

## Rules
- Never modify running containers
- Deploy new versions instead of patching
- Use versioned container images
- Treat infrastructure as disposable

## Analysis
This skill enforces immutable infrastructure principles for predictable deployments. Never modifying running containers prevents configuration drift and ensures all instances are identical. Deploying new versions rather than patching provides clear rollback paths and audit trails. Versioned images enable precise tracking of what's running in each environment. Treating infrastructure as disposable (cattle, not pets) enables automated scaling and recovery. Immutable infrastructure simplifies operations, improves reliability, and supports continuous delivery practices, though it requires robust automation and may increase deployment frequency compared to traditional patch-in-place approaches.
