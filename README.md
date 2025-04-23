# Golang-Python Fast Communication

This project demonstrates efficient communication between a Golang API and a Python service using shared memory for data exchange, with a focus on performance comparison between REST API and shared memory approaches.

## Project Structure

```
.
├── golang-api/           # Golang API service
│   └── main.go          # Golang API implementation
├── python-api/           # Python service
│   └── main.py          # Python implementation
└── shared_memory_dir/    # Directory for shared memory files
```

## Features

- Two communication methods:
  1. Direct HTTP API calls
  2. Shared memory with HTTP signaling
- Efficient data transfer using memory-mapped files
- Automatic cleanup of shared memory resources
- Detailed logging for debugging and performance monitoring
- Performance comparison between communication methods

## Prerequisites

- Go 1.16 or higher
- Python 3.7 or higher
- Basic understanding of HTTP APIs and shared memory concepts

## Setup and Running

1. Start the Python service:
```bash
cd python-api
python main.py
```

2. Start the Golang API:
```bash
cd golang-api
go run main.go
```

## API Endpoints

### Golang API (Port 8080)

- `/api/users-via-api`: Get users via direct HTTP API call
- `/api/users-via-shm`: Get users via shared memory

### Python Service (Port 5000)

- `/api/users`: Returns user data directly
- `/api/write-to-shm`: Writes user data to shared memory

## Testing

Test the endpoints using curl:

```bash
# Direct API call
curl http://localhost:8080/api/users-via-api

# Shared memory communication
curl http://localhost:8080/api/users-via-shm
```

## Performance Analysis

### Communication Methods Comparison

1. **REST API Approach** (`/api/users-via-api`):
   - Data flow:
     1. Python serialization to JSON
     2. Network transfer over HTTP
     3. Go deserialization from JSON
   - Best for: Small payloads (few KB)
   - Advantages:
     - Simple to implement
     - Standard HTTP protocol
     - Good for small data transfers
     - Built-in error handling

2. **Shared Memory Approach** (`/api/users-via-shm`):
   - Data flow:
     1. Python serialization to JSON
     2. Direct memory write
     3. Go deserialization from JSON
   - Best for: Large payloads (MBs)
   - Advantages:
     - Faster for large data transfers
     - No network serialization overhead
     - Direct memory access
     - Avoids HTTP protocol overhead

### Performance Trade-offs

- **Small Payload Size** (e.g., 2 users with basic info):
  - REST API performs better because:
    - Shared memory setup overhead is relatively high
    - HTTP requests for small payloads are efficient
    - Serialization/deserialization overhead is minimal
    - Network latency is negligible

- **Large Payload Size** (e.g., 100 users with detailed info):
  - Shared Memory performs better because:
    - Setup overhead becomes negligible
    - No network serialization/deserialization
    - Direct memory access is faster than network
    - Avoids HTTP protocol overhead

## Implementation Details

- Current implementation uses temporary files for shared memory
- Shared memory size is configurable (default: 2MB)
- Automatic cleanup of shared memory resources
- Comprehensive error handling and logging

## Future Optimizations

- Unix domain sockets for signaling
- Persistent shared memory
- Memory-mapped files with proper synchronization
- Compression for large payloads
- Connection pooling for REST API
- Caching mechanisms

## Error Handling

- Both services include comprehensive error handling
- Logs are provided for debugging
- Shared memory files are automatically cleaned up
- HTTP errors are properly propagated

## Contributing

Feel free to submit issues and enhancement requests. 