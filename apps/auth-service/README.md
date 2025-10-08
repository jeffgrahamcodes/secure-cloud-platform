# Auth Service

Simple JWT-based authentication microservice for the secure-cloud-platform.

## Features

- JWT token generation
- Token validation
- Token refresh
- Health check endpoint
- Docker containerized

## API Endpoints

### Health Check

```bash
GET /health
```

**Response:**

```json
{
  "status": "healthy",
  "service": "auth-service",
  "timestamp": "2025-10-07T12:00:00.000Z"
}
```

### Login

```bash
POST /auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Success Response:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

**Error Response:**

```json
{
  "error": "Invalid credentials"
}
```

### Verify Token

```bash
POST /auth/verify
Authorization: Bearer <token>
```

**Success Response:**

```json
{
  "valid": true,
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

### Refresh Token

```bash
POST /auth/refresh
Authorization: Bearer <token>
```

**Response:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Local Development

### Prerequisites

- Node.js 18+
- Docker (optional)

### Setup

```bash
# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Update .env with your values (or use defaults for development)

# Run locally
node index.js
```

The service will start on port 3001 (or the PORT specified in .env).

### With Docker

```bash
# Build the image
docker build -t auth-service .

# Run the container
docker run -p 3001:3001 auth-service

# Or with custom environment variables
docker run -p 3001:3001 -e JWT_SECRET=my-secret auth-service
```

## Testing

```bash
# Health check
curl http://localhost:3001/health

# Login to get a token
curl -X POST http://localhost:3001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Verify token (replace YOUR_TOKEN with actual token from login)
curl -X POST http://localhost:3001/auth/verify \
  -H "Authorization: Bearer YOUR_TOKEN"

# Refresh token
curl -X POST http://localhost:3001/auth/refresh \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test invalid credentials
curl -X POST http://localhost:3001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"wrong"}'
```

## Environment Variables

| Variable     | Description                | Default                                | Required         |
| ------------ | -------------------------- | -------------------------------------- | ---------------- |
| `PORT`       | Server port                | 3001                                   | No               |
| `JWT_SECRET` | Secret key for JWT signing | `your-secret-key-change-in-production` | Yes (production) |

**Security Note:** The default JWT_SECRET is for development only. Always use a strong, randomly generated secret in production.

## Test Users

For development/testing purposes:

| Username | Password | Role  |
| -------- | -------- | ----- |
| admin    | admin123 | admin |
| user     | user123  | user  |

**NOTE:** These are mock users for development only. In production, use a proper database with hashed passwords.

## Security Considerations

This is a learning/demonstration project. For production use, implement:

- **Password hashing** - Use bcrypt to hash passwords
- **Database integration** - Store users in PostgreSQL/MongoDB
- **Rate limiting** - Prevent brute force attacks on login
- **HTTPS only** - Never transmit tokens over HTTP
- **Token rotation** - Implement refresh token rotation
- **Secret management** - Use AWS Secrets Manager or Kubernetes Secrets
- **Password requirements** - Enforce complexity rules
- **Account lockout** - Lock accounts after failed attempts
- **Audit logging** - Log all authentication events
- **Token expiration** - Use short-lived access tokens with refresh tokens

## Technology Stack

- **Runtime:** Node.js 18
- **Framework:** Express.js
- **Authentication:** JSON Web Tokens (JWT)
- **Container:** Docker (Alpine Linux base)

## Architecture Notes

This service is designed to be:

- **Stateless** - Can scale horizontally
- **Independent** - No dependencies on other services
- **Cloud-native** - Ready for Kubernetes deployment
- **Secure by default** - Security considerations documented

## Roadmap

- [ ] Connect to PostgreSQL database
- [ ] Implement password hashing with bcrypt
- [ ] Add rate limiting middleware
- [ ] Implement refresh token rotation
- [ ] Add OAuth2/OIDC support
- [ ] Add multi-factor authentication (MFA)
- [ ] Implement role-based access control (RBAC)
- [ ] Add Prometheus metrics endpoint

## Contributing

This is a learning project. Feedback and suggestions welcome!

## License

MIT

---

**Part of the [secure-cloud-platform](../../README.md) project**
