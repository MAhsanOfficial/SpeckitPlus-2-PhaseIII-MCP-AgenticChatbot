# Environment Variables Best Practices

## Rules
- Use ConfigMaps for non-sensitive configuration
- Use Secrets for sensitive data
- Validate required environment variables at startup
- Document all environment variables

## Analysis
This skill establishes proper environment variable management in containerized applications. ConfigMaps separate configuration from code, enabling the same image to run in different environments. Secrets provide basic protection for sensitive data like API keys and database passwords. Startup validation fails fast if required configuration is missing, preventing runtime errors. Documentation helps operators understand configuration requirements and troubleshoot issues. Environment variables follow the twelve-factor app methodology, though complex configuration may benefit from configuration files mounted as volumes instead of individual environment variables.
