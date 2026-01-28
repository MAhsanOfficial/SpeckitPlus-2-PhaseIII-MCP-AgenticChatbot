# Phase Safety

## Rules
- No modification of Phase III app logic
- Only infra & deployment layers allowed

## Analysis
This skill enforces strict boundaries between application code and infrastructure during Phase IV deployment work. Phase III represents the working application logic that has been tested and validated. Modifying this code during infrastructure deployment introduces unnecessary risk and violates separation of concerns. Infrastructure and deployment layers (Dockerfiles, Kubernetes manifests, Helm charts, CI/CD pipelines) can be freely modified to containerize and deploy the application. This boundary ensures that deployment issues can be isolated from application bugs, simplifies rollback procedures, and maintains the integrity of the tested application codebase. Any required application changes should be tracked separately and implemented in a future phase with proper testing.
