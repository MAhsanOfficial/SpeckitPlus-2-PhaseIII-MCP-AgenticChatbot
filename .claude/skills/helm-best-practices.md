# Helm Best Practices

## Rules
- Parameterize all environment-specific values
- Use values.yaml for configuration
- Version charts semantically
- Include NOTES.txt for deployment guidance

## Analysis
This skill enforces Helm chart development best practices for maintainable Kubernetes deployments. Parameterizing environment-specific values through templates enables the same chart to deploy across dev, staging, and production with different configurations. Centralizing configuration in values.yaml provides a single source of truth and simplifies overrides. Semantic versioning of charts enables safe upgrades and clear communication of breaking changes. NOTES.txt files guide operators through post-deployment steps and provide essential information about accessing the deployed application.
