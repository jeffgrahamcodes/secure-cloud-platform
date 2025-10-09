# Worker Service

Background job processing service for the secure-cloud-platform. Handles asynchronous tasks like email sending, image processing, data synchronization, and report generation.

## Features

- Asynchronous job processing
- Job status tracking
- Worker statistics
- Multiple job types
- Health monitoring
- Docker containerized

## Job Types

| Type        | Duration | Description                     |
| ----------- | -------- | ------------------------------- |
| `email`     | 2s       | Send email notifications        |
| `image`     | 5s       | Process and optimize images     |
| `data_sync` | 3s       | Synchronize data across systems |
| `report`    | 4s       | Generate reports                |

## API Endpoints

### Health Check

```bash
GET /health
```

**Response:**

```json
{
  "status": "healthy",
  "service": "worker-service",
  "timestamp": "2025-10-08T12:00:00",
  "queue_size": 2,
  "total_jobs": 15
}
```

### Create Job

```bash
POST /jobs
Content-Type: application/json

{
  "type": "email"
}
```

**Response:**

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "email",
  "status": "queued",
  "message": "Job created and queued for processing"
}
```

### Get Job Status

```bash
GET /jobs/{job_id}
```

**Response:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "email",
  "description": "Send email",
  "status": "completed",
  "created_at": "2025-10-08T12:00:00",
  "started_at": "2025-10-08T12:00:01",
  "completed_at": "2025-10-08T12:00:03"
}
```

### List All Jobs

```bash
GET /jobs
```

**Response:**

```json
{
  "total": 25,
  "queue_size": 3,
  "jobs": [...]
}
```

### Get Worker Statistics

```bash
GET /stats
```

**Response:**

```json
{
  "total_jobs": 25,
  "completed": 20,
  "processing": 2,
  "queued": 3,
  "failed": 0,
  "queue_size": 3,
  "available_job_types": ["email", "image", "data_sync", "report"]
}
```

## Local Development

### Prerequisites

- Python 3.11+
- Docker (optional)

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

The service will start on port 3002.

### With Docker

```bash
# Build the image
docker build -t worker-service .

# Run the container
docker run -p 3002:3002 worker-service
```

## Testing

```bash
# Health check
curl http://localhost:3002/health

# Create a job
curl -X POST http://localhost:3002/jobs \
  -H "Content-Type: application/json" \
  -d '{"type":"email"}'

# Check job status (use job_id from previous response)
curl http://localhost:3002/jobs/{job_id}

# Create multiple jobs
curl -X POST http://localhost:3002/jobs \
  -H "Content-Type: application/json" \
  -d '{"type":"image"}'

curl -X POST http://localhost:3002/jobs \
  -H "Content-Type: application/json" \
  -d '{"type":"data_sync"}'

# View all jobs
curl http://localhost:3002/jobs

# Check worker stats
curl http://localhost:3002/stats

# Try invalid job type (should return error)
curl -X POST http://localhost:3002/jobs \
  -H "Content-Type: application/json" \
  -d '{"type":"invalid"}'
```

## Architecture

- **Flask** web framework for REST API
- **Threading** for background job processing
- **Queue** for job management (in-memory for demo)
- **UUID** for unique job identifiers
- **Logging** for observability

## Production Considerations

This is a demonstration/learning project. For production use, implement:

- ✅ **Message queue** - Replace in-memory queue with Redis, RabbitMQ, or AWS SQS
- ✅ **Database** - Persist job status in PostgreSQL/MongoDB
- ✅ **Horizontal scaling** - Multiple worker instances
- ✅ **Job retries** - Automatic retry logic for failed jobs
- ✅ **Dead letter queue** - Handle permanently failed jobs
- ✅ **Monitoring** - Prometheus metrics for queue depth, processing time
- ✅ **Rate limiting** - Prevent queue overflow
- ✅ **Job priority** - Priority queue implementation
- ✅ **Authentication** - Secure job creation endpoint
- ✅ **Idempotency** - Prevent duplicate job processing
- ✅ **Graceful shutdown** - Complete in-flight jobs before stopping
- ✅ **Circuit breakers** - Handle downstream service failures

## Next Steps

- [ ] Integrate with Redis for persistent queue
- [ ] Add job retries and exponential backoff
- [ ] Implement job priority levels
- [ ] Add Prometheus metrics endpoint
- [ ] Connect to API/Auth services for real workflows
- [ ] Add webhook notifications on job completion
- [ ] Implement job cancellation
- [ ] Add job scheduling (cron-like functionality)

## Technology Stack

- **Runtime:** Python 3.11
- **Framework:** Flask
- **Job Queue:** Python Queue (in-memory)
- **Container:** Docker (Python slim base)
- **Threading:** Python threading module

## Security Notes

- Jobs are processed in-memory (not persisted)
- No authentication on endpoints (add in production)
- Suitable for demonstration and development only
- Production systems should use proper message queues and authentication

---

**Part of the [secure-cloud-platform](../../README.md) project**
