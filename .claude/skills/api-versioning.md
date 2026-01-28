# API Versioning

## Rules
- Version APIs in URL path or headers
- Maintain backward compatibility
- Deprecate old versions with notice period
- Document breaking changes clearly

## Analysis
This skill ensures smooth API evolution without breaking existing clients. URL path versioning (e.g., /v1/users) provides clear version visibility, while header-based versioning keeps URLs clean. Maintaining backward compatibility within a version allows bug fixes and feature additions without forcing client updates. Deprecation with notice periods gives clients time to migrate, typically 6-12 months for public APIs. Clear documentation of breaking changes helps clients plan migrations and reduces support burden, though it requires discipline in change management.
