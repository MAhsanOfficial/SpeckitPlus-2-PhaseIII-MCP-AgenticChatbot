# Init Containers and Sidecars

## Rules
- Use init containers for setup tasks
- Implement sidecars for cross-cutting concerns
- Keep sidecar resource usage minimal
- Document sidecar responsibilities clearly

## Analysis
This skill establishes proper use of init containers and sidecar patterns. Init containers run before main containers, handling setup tasks like database migrations, configuration fetching, or dependency checks. Sidecars run alongside main containers, implementing cross-cutting concerns like logging agents, proxies, or monitoring exporters. Minimal resource usage for sidecars prevents them from consuming resources needed by the main application. Clear documentation of sidecar responsibilities helps teams understand pod composition and troubleshoot issues, though excessive sidecars can complicate pod management.
