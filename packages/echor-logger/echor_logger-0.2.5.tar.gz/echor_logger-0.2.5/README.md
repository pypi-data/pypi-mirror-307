# EchorTech Logging

A robust logging middleware for applications that provides structured logging with correlation IDs, trace IDs, and standardized log formats.

## Installation

```bash
pip install echor-logger
```

## Features

- 🔍 Structured logging for applications
- 📊 Support for info, warn, and error log levels
- 🔗 Automatic correlation ID and trace ID tracking
- ⏱️ Request timing and response metrics
- 🏷️ Custom tagging support
- 🛡️ Middleware for request context preservation
- 🚀 Easy integration with FastAPI

## Quick Start

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from echor_logger import echorLogger
import uuid

app = FastAPI()

class TraceIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.trace_id = str(uuid.uuid4())
        request.state.correlation_id = str(uuid.uuid4())
        response = await call_next(request)
        return response

app.add_middleware(TraceIdMiddleware)

@app.get("/success")
async def success_route(request: Request):
    data = {
        "statusCode": 200,
        "message": "This is a success message",
        "responseTime": 123,
        "result": {"key": "value"}
    }

    modified_request = {
        'info': {'received': None},
        'traceId': request.state.trace_id,
        'correlationId': request.state.correlation_id,
        'auth': {'credentials': {'sub': 'user123'}},
        'method': request.method,
        'url': str(request.url)
    }

    echorLogger.info(modified_request, ['SUCCESS_TAG'], data)
    return data
```

## Detailed Usage Examples

### Warning Logging
```python
@app.get("/warn")
async def warn_route(request: Request):
    data = {
        "statusCode": 200,
        "message": "This is a warning message",
        "responseTime": 150,
        "result": {"key": "warning-value"}
    }

    modified_request = {
        'info': {'received': None},
        'traceId': request.state.trace_id,
        'correlationId': request.state.correlation_id,
        'auth': {'credentials': {'sub': 'user123'}},
        'method': request.method,
        'url': str(request.url)
    }

    echorLogger.warn(modified_request, ['WARN_TAG'], data)
    return data
```

### Error Logging
```python
@app.get("/error")
async def error_route(request: Request):
    try:
        # Simulated error scenario
        raise Exception("Simulated error occurred")
    except Exception as error:
        data = {
            'statusCode': 500,
            'message': 'An error occurred',
            'errorCode': 'ERR_SIMULATION',
            'responseTime': 200
        }
        
        modified_request = {
            'info': {'received': None},
            'traceId': request.state.trace_id,
            'correlationId': request.state.correlation_id,
            'auth': {'credentials': {'sub': 'user123'}},
            'method': request.method,
            'url': str(request.url)
        }

        echorLogger.error(modified_request, ['ERROR_TAG'], data, error)
        return {"error": "An error occurred"}
```

## API Reference

### Logging Methods

#### `echorLogger.info(request_context, tags, data)`
Logs information level messages.

#### `echorLogger.warn(request_context, tags, data)`
Logs warning level messages.

#### `echorLogger.error(request_context, tags, data, error)`
Logs error level messages with error stack traces.

## Request Context Structure

```python
{
    'info': {'received': None},
    'traceId': 'unique-trace-id',
    'correlationId': 'unique-correlation-id',
    'auth': {
        'credentials': {
            'sub': 'user_identifier'
        }
    },
    'method': 'HTTP_METHOD',
    'url': 'request_url'
}
```

## Response Data Structure

### Success Response
```python
{
    'statusCode': 200,
    'message': 'Success message',
    'responseTime': 123,
    'result': {'key': 'value'}
}
```

### Error Response
```python
{
    'statusCode': 500,
    'message': 'Error message',
    'errorCode': 'ERR_CODE',
    'responseTime': 200
}
```

## Dependencies

- python-dotenv