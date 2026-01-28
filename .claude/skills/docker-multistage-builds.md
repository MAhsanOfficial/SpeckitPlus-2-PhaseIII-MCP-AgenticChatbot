# Docker Multi-Stage Builds

## Rules
- Separate build and runtime stages
- Use builder pattern for compiled languages
- Copy only necessary artifacts to final image
- Minimize final image layers

## Analysis
This skill optimizes container images through multi-stage builds. Separating build and runtime stages keeps build tools and dependencies out of the final image, significantly reducing size and attack surface. The builder pattern compiles code in one stage and copies only the executable to a minimal runtime image. Selective artifact copying ensures only production-necessary files are included, excluding source code, tests, and build caches. Minimizing layers in the final stage improves pull performance and reduces storage costs while maintaining image clarity and debuggability.
