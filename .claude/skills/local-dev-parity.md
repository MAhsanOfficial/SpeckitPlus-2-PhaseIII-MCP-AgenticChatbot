# Local Development Parity

## Rules
- Minikube mirrors production architecture
- Use same container images locally and in production
- Test Helm charts in local cluster before deployment
- Maintain environment-specific values files

## Analysis
This skill ensures development-production parity, reducing "works on my machine" issues. Minikube provides a local Kubernetes cluster that closely mimics production behavior, enabling realistic testing of deployments, services, and networking. Using identical container images across environments eliminates image-related discrepancies. Testing Helm charts locally catches configuration errors before they reach production, reducing deployment failures. Environment-specific values files allow the same chart to be tested with local configurations while maintaining production-ready templates.
