# Testing in Kubernetes

## Rules
- Unit test application logic independently
- Integration test with test containers
- Smoke test deployments in staging
- Load test before production rollout

## Analysis
This skill establishes comprehensive testing strategies for Kubernetes applications. Unit tests validate business logic without infrastructure dependencies, enabling fast feedback. Integration tests with test containers (like Testcontainers) verify database interactions and external dependencies in isolated environments. Smoke tests in staging validate that deployments work in a production-like cluster, catching configuration and networking issues. Load testing identifies performance bottlenecks and capacity limits before they impact users, informing resource allocation and autoscaling configuration.
