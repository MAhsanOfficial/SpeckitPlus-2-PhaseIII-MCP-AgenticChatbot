# Session Management

## Rules
- Use stateless JWT tokens for authentication
- Store session data in distributed cache
- Implement session timeout and renewal
- Secure session tokens with HttpOnly and Secure flags

## Analysis
This skill establishes secure session management in distributed systems. Stateless JWT tokens eliminate server-side session storage, enabling horizontal scaling without session affinity. Distributed cache storage (Redis) enables session sharing across pods when server-side sessions are necessary. Session timeout and renewal balance security with user experience. HttpOnly and Secure flags protect tokens from XSS and man-in-the-middle attacks, though JWT revocation requires additional infrastructure like token blacklists or short expiration times.
