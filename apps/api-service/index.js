const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'api-service',
    timestamp: new Date().toISOString(),
  });
});

// Simple users API
app.get('/api/users', (req, res) => {
  res.json({
    users: [
      { id: 1, name: 'Alice', role: 'admin' },
      { id: 2, name: 'Bob', role: 'user' },
    ],
  });
});

app.listen(PORT, () => {
  console.log(`🚀 API Service running on port ${PORT}`);
});
