# Database Migration Strategy

## Rules
- Use init containers for schema migrations
- Implement backward-compatible schema changes
- Test migrations with production-like data volumes
- Maintain rollback scripts for every migration

## Analysis
This skill ensures safe database evolution in production environments. Init containers run migrations before application pods start, ensuring schema readiness. Backward-compatible changes (additive columns, new tables) allow old and new code versions to coexist during rolling deployments. Testing with production-like data volumes identifies performance issues before they impact users. Rollback scripts enable quick recovery from problematic migrations, though some changes (like dropping columns) may be irreversible and require careful planning.
