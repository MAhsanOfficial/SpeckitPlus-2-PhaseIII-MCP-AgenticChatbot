# Security & JWT Handling

## Capabilities
- JWT decoding & verification
- Enforce user isolation
- Token expiration handling
- Secure API filtering

## Analysis
This skill establishes the security boundary for the application. JWT handling ensures that only authenticated requests are processed. User isolation is a critical integrity requirement, ensuring that users can only access their own data. Token expiration management maintains session security without compromising user experience. Secure API filtering prevents unauthorized data exposure at the database query level by injecting user identity context into every filter.
