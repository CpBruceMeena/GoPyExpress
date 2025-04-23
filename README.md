# Golang-Python Fast Communication

This project demonstrates efficient communication between a Golang API and a Python service using shared memory for data exchange.

## Project Structure

```
.
├── golang-api/           # Golang API service
│   └── cmd/
│       └── api/
│           └── main.go   # Golang API implementation
└── python-shared-memory/ # Python service
    └── main.py          # Python implementation
```

## Features

- Two communication methods:
  1. Direct HTTP API calls
  2. Shared memory with HTTP signaling
- Efficient data transfer using memory-mapped files
- Automatic cleanup of shared memory resources
- Detailed logging for debugging and performance monitoring

## Prerequisites

- Go 1.16 or higher
- Python 3.7 or higher
- Basic understanding of HTTP APIs and shared memory concepts

## Setup and Running

1. Start the Python service:
```bash
cd python-shared-memory
python main.py
```

2. Start the Golang API:
```bash
cd golang-api
go run cmd/api/main.go
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

## Performance Considerations

- The shared memory approach involves:
  1. HTTP request to trigger data write
  2. File I/O operations for shared memory
  3. Data cleanup after reading
- Current implementation uses temporary files for shared memory
- Future optimizations could include:
  - Unix domain sockets for signaling
  - Persistent shared memory
  - Memory-mapped files with proper synchronization

## Error Handling

- Both services include comprehensive error handling
- Logs are provided for debugging
- Shared memory files are automatically cleaned up
- HTTP errors are properly propagated

## Contributing

Feel free to submit issues and enhancement requests. 