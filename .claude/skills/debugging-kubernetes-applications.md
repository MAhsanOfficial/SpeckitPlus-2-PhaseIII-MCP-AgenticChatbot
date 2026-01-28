# Debugging Kubernetes Applications

## Rules
- Use kubectl logs for application logs
- Use kubectl describe for resource events
- Use kubectl exec for interactive debugging
- Enable debug logging in non-production

## Analysis
This skill establishes systematic debugging approaches for Kubernetes applications. kubectl logs retrieves container stdout/stderr, the primary source of application-level debugging information. kubectl describe shows resource events, revealing scheduling failures, image pull errors, and health check failures. kubectl exec enables interactive debugging by running commands inside containers, useful for inspecting filesystem state or running diagnostic tools. Debug logging in non-production provides detailed information for troubleshooting without impacting production performance. Effective debugging requires understanding both application behavior and Kubernetes resource lifecycle.
