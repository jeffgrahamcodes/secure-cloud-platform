# API Service

REST API service for the secure-cloud-platform. Provides core application endpoints and serves as the main entry point for client applications.

## Features

- RESTful API endpoints
- Health check monitoring
- User management (demo)
- Dockerized deployment
- Production-ready health checks

## API Endpoints

### Health Check

```bash
GET /health
```

**Response:**

```json
{
  "status": "healthy",
  "service": "api-service",
  "timestamp": "2025-10-08T12:00:00.000Z"
}
```

### List Users

```bash
GET /api/users
```

**Response:**

```json
{
  "users": [
    { "id": 1, "name": "Alice", "role": "admin" },
    { "id": 2, "name": "Bob", "role": "user" }
  ]
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

# Run locally
node index.js
```

The service will start on port 3000 (or the PORT specified in environment variables).

### With Docker

```bash
# Build the image
docker build -t api-service .

# Run the container
docker run -p 3000:3000 api-service

# Or with custom port
docker run -p 8080:3000 -e PORT=3000 api-service
```

## Testing

```bash
# Health check
curl http://localhost:3000/health

# Get users
curl http://localhost:3000/api/users
```

## Environment Variables

| Variable | Description | Default | Required |
| -------- | ----------- | ------- | -------- |
| `PORT`   | Server port | 3000    | No       |

## Architecture

- **Express.js** - Lightweight web framework
- **Node.js 18** - Runtime environment
- **Alpine Linux** - Minimal container base image

## Production Considerations

This is a demonstration/learning project. For production use, implement:

- **Database integration** - Connect to PostgreSQL/MongoDB for data persistence
- **Authentication middleware** - Integrate with auth-service for token validation
- **Rate limiting** - Prevent API abuse
- **Request validation** - Validate and sanitize all inputs
- **Error handling** - Comprehensive error middleware
- **Logging** - Structured logging with correlation IDs
- **API versioning** - Support multiple API versions
- **CORS configuration** - Proper cross-origin resource sharing
- **Compression** - Gzip/Brotli response compression
- **Caching** - Redis for frequently accessed data
- **Monitoring** - APM integration for performance tracking
- **Documentation** - OpenAPI/Swagger specification

## Docker Health Check

The container includes a health check that runs every 30 seconds:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3
```

This allows orchestrators like Kubernetes to:

- Know when the container is ready to receive traffic
- Restart unhealthy containers automatically
- Route traffic only to healthy instances

## Security Notes

- Currently uses mock data (no database)
- No authentication on endpoints (integrate with auth-service)
- Suitable for demonstration and development only
- Production deployments require proper security measures

## Next Steps

- [ ] Connect to PostgreSQL database
- [ ] Add authentication middleware (integrate auth-service)
- [ ] Implement request validation with Joi or Zod
- [ ] Add rate limiting middleware
- [ ] Create OpenAPI documentation
- [ ] Add unit and integration tests
- [ ] Implement CORS properly
- [ ] Add structured logging
- [ ] Create additional resource endpoints (orders, products, etc.)

## Technology Stack

- **Runtime:** Node.js 18
- **Framework:** Express.js
- **Container:** Docker (Alpine Linux base)

## Project Structure

```
api-service/
├── index.js              # Main application file
├── package.json          # Dependencies
├── Dockerfile            # Container definition
├── .dockerignore         # Docker build exclusions
└── README.md             # This file
```

---

**Part of the [secure-cloud-platform](../../README.md) project**
