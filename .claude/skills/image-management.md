# Image Management

## Rules
- Use private registries for proprietary images
- Implement image scanning in CI/CD
- Tag images with Git commit SHAs
- Implement image pull secrets per namespace

## Analysis
This skill establishes secure and reliable container image management. Private registries protect proprietary code and provide control over image distribution. Image scanning in CI/CD identifies vulnerabilities before deployment, shifting security left. Git commit SHA tags provide precise version tracking and enable correlation between deployed code and source control. Image pull secrets per namespace follow least privilege, limiting registry access to only necessary namespaces, though secret management across namespaces requires careful coordination.
