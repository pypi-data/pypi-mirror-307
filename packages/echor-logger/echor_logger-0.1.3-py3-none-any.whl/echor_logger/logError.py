import json
import os
import platform
from datetime import datetime

from dotenv import load_dotenv

from util.formatTimestamp import formatTimestamp

load_dotenv()

SERVICE_NAME = os.getenv('SERVICE_NAME', 'unknown-service')


def log_error(request, error_tags, data, error=None):
    timestamp = formatTimestamp(request.get('info', {}).get('received'))
    hostname = platform.node()
    process_id = os.getpid()
    machine_id = f"{int(datetime.utcnow().timestamp())}:{hostname}:{process_id}"
    tags = list(set(['ERROR'] + error_tags))
    correlations = {
        "user-agent": request['headers'].get('user-agent', 'unknown'),
        "x-correlation-id": request.get('correlationId', 'unknown'),
        "x-trace-id": request.get('traceId', 'unknown'),
        "service": SERVICE_NAME
    }

    log_data = {
        "timeStamp": timestamp,
        "subject": request.get('auth', {}).get('credentials', {}).get('sub'),
        "statusCode": data.get('statusCode'),
        "error": str(error) if error else data.get('error'),
        "message": data.get('message'),
        "errorCode": data.get('errorCode'),
        "method": request.get('method'),
        "uri": request.get('url'),
        "responseTime": data.get('responseTime')
    }

    print(
        f"{timestamp}, ({machine_id}) [{','.join(tags)}], {{\"correlations\": {json.dumps(correlations)}}}, data: {json.dumps(log_data)}")
