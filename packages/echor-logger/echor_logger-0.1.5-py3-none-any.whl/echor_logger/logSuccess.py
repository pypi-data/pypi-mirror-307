import json
import os
import platform
from datetime import datetime

from dotenv import load_dotenv

from .util.formatTimestamp import formatTimestamp

load_dotenv()

SERVICE_NAME = os.getenv('SERVICE_NAME', 'unknown-service')
print(SERVICE_NAME, 'service name')


def log_success(request, success_tags, data):
    timestamp = formatTimestamp(request.get('info', {}).get('received'))
    hostname = platform.node()  # Use platform.node() for cross-platform compatibility
    process_id = os.getpid()
    machine_id = f"{int(datetime.utcnow().timestamp())}:{hostname}:{process_id}"
    tags = list(set(['INFO'] + success_tags))
    correlations = {
        "user-agent": request['headers'].get('user-agent', 'unknown'),
        "x-correlation-id": request.get('correlationId', 'unknown'),
        "x-trace-id": request.get('traceId', 'unknown'),
        "service": SERVICE_NAME
    }

    log_data = {
        "timeStamp": timestamp,
        "subject": request.get('auth', {}).get('credentials', {}).get('sub'),
        "statusCode": data.get('statusCode', 200),
        "message": data.get('message', 'Operation completed successfully'),
        "method": request.get('method'),
        "uri": request.get('url'),
        "responseTime": data.get('responseTime'),
        "responseData": data.get('result')
    }

    print(
        f"{timestamp}, ({machine_id}) [{','.join(tags)}], {{\"correlations\": {json.dumps(correlations)}}}, data: {json.dumps(log_data)}")


def log_warn(request, success_tags, data):
    timestamp = formatTimestamp(request.get('info', {}).get('received'))
    hostname = platform.node()  # Use platform.node() for cross-platform compatibility
    process_id = os.getpid()
    machine_id = f"{int(datetime.utcnow().timestamp())}:{hostname}:{process_id}"
    tags = list(set(['WARN'] + success_tags))
    correlations = {
        "user-agent": request['headers'].get('user-agent', 'unknown'),
        "x-correlation-id": request.get('correlationId', 'unknown'),
        "x-trace-id": request.get('traceId', 'unknown'),
        "service": SERVICE_NAME
    }

    log_data = {
        "timeStamp": timestamp,
        "subject": request.get('auth', {}).get('credentials', {}).get('sub'),
        "statusCode": data.get('statusCode', 200),
        "message": data.get('message', 'Operation completed successfully'),
        "method": request.get('method'),
        "uri": request.get('url'),
        "responseTime": data.get('responseTime'),
        "responseData": data.get('result')
    }

    print(
        f"{timestamp}, ({machine_id}) [{','.join(tags)}], {{\"correlations\": {json.dumps(correlations)}}}, data: {json.dumps(log_data)}")
