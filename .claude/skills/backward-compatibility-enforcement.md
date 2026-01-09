# Backward Compatibility Enforcement

## Rules
- Never modify Phase II task APIs
- Never change database schema unless explicitly extended
- Add new tables only if required
- No breaking migrations

## Analysis
This skill ensures Phase III features integrate seamlessly without disrupting existing functionality. By prohibiting modifications to Phase II APIs and database schema changes, it protects the stability of core todo/habit operations. New tables are only added when absolutely necessary, and all migrations must be backward-compatible to prevent data loss or service disruption during deployments.
