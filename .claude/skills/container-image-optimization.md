# Container Image Optimization

## Rules
- Minimize image layers
- Use .dockerignore to exclude unnecessary files
- Leverage build cache effectively
- Remove build dependencies from final image

## Analysis
This skill optimizes container images for size and build speed. Minimizing layers reduces image size and improves pull performance, achieved by combining related commands. .dockerignore prevents unnecessary files (node_modules, .git, tests) from being copied into the image, reducing size and build time. Effective cache usage (ordering commands from least to most frequently changed) speeds up rebuilds. Removing build dependencies through multi-stage builds keeps final images minimal, reducing attack surface and storage costs while maintaining fast builds through layer caching.
