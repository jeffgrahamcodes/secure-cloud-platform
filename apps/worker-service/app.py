from flask import Flask, jsonify, request
import time
import threading
import uuid
from datetime import datetime
from queue import Queue
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Simulated job queue
job_queue = Queue()
job_status = {}

# Job processing types
JOB_TYPES = {
    'email': {'duration': 2, 'description': 'Send email'},
    'image': {'duration': 5, 'description': 'Process image'},
    'data_sync': {'duration': 3, 'description': 'Sync data'},
    'report': {'duration': 4, 'description': 'Generate report'}
}

def process_job(job_id, job_type):
    """Simulate processing a job"""
    try:
        logger.info(f"Starting job {job_id} - Type: {job_type}")
        job_status[job_id]['status'] = 'processing'
        job_status[job_id]['started_at'] = datetime.now().isoformat()

        # Simulate work with sleep
        duration = JOB_TYPES.get(job_type, {}).get('duration', 2)
        time.sleep(duration)

        # Mark as completed
        job_status[job_id]['status'] = 'completed'
        job_status[job_id]['completed_at'] = datetime.now().isoformat()
        logger.info(f"Completed job {job_id}")

    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")
        job_status[job_id]['status'] = 'failed'
        job_status[job_id]['error'] = str(e)

def worker():
    """Background worker that processes jobs from queue"""
    logger.info("Worker thread started")
    while True:
        if not job_queue.empty():
            job_id, job_type = job_queue.get()
            process_job(job_id, job_type)
            job_queue.task_done()
        else:
            time.sleep(1)

# Start background worker thread
worker_thread = threading.Thread(target=worker, daemon=True)
worker_thread.start()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'worker-service',
        'timestamp': datetime.now().isoformat(),
        'queue_size': job_queue.qsize(),
        'total_jobs': len(job_status)
    }), 200

@app.route('/jobs', methods=['POST'])
def create_job():
    """Create a new job"""
    data = request.get_json()

    if not data or 'type' not in data:
        return jsonify({'error': 'Job type required'}), 400

    job_type = data['type']

    if job_type not in JOB_TYPES:
        return jsonify({
            'error': f'Invalid job type. Valid types: {list(JOB_TYPES.keys())}'
        }), 400

    # Create job
    job_id = str(uuid.uuid4())
    job_status[job_id] = {
        'id': job_id,
        'type': job_type,
        'description': JOB_TYPES[job_type]['description'],
        'status': 'queued',
        'created_at': datetime.now().isoformat()
    }

    # Add to queue
    job_queue.put((job_id, job_type))

    logger.info(f"Created job {job_id} - Type: {job_type}")

    return jsonify({
        'job_id': job_id,
        'type': job_type,
        'status': 'queued',
        'message': 'Job created and queued for processing'
    }), 201

@app.route('/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Get status of a specific job"""
    if job_id not in job_status:
        return jsonify({'error': 'Job not found'}), 404

    return jsonify(job_status[job_id]), 200

@app.route('/jobs', methods=['GET'])
def list_jobs():
    """List all jobs"""
    return jsonify({
        'total': len(job_status),
        'queue_size': job_queue.qsize(),
        'jobs': list(job_status.values())
    }), 200

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get worker statistics"""
    completed = sum(1 for job in job_status.values() if job['status'] == 'completed')
    processing = sum(1 for job in job_status.values() if job['status'] == 'processing')
    queued = sum(1 for job in job_status.values() if job['status'] == 'queued')
    failed = sum(1 for job in job_status.values() if job['status'] == 'failed')

    return jsonify({
        'total_jobs': len(job_status),
        'completed': completed,
        'processing': processing,
        'queued': queued,
        'failed': failed,
        'queue_size': job_queue.qsize(),
        'available_job_types': list(JOB_TYPES.keys())
    }), 200

if __name__ == '__main__':
    port = 3002
    logger.info(f"🐍 Worker Service starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)