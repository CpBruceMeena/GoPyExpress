# Golang-Python Fast Communication

This project demonstrates efficient communication between a Golang API and a Python service using shared memory for data exchange, with a focus on performance comparison between REST API and shared memory approaches.

## Project Structure

```
.
├── golang-api/           # Golang API service
│   └── main.go          # Golang API implementation
├── python-api/           # Python service
│   └── main.py          # Python implementation
├── load-testing/         # Load testing setup using Locust
│   ├── locustfile.py    # Load test configuration
│   ├── requirements.txt # Python dependencies
│   └── README.md        # Load testing documentation
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

The project includes comprehensive load testing results comparing both communication methods. See [LOAD_TEST_RESULTS.md](LOAD_TEST_RESULTS.md) for detailed analysis of:

- Throughput comparison
- Response time analysis
- Error rates
- Performance recommendations
- Future optimization suggestions

Key findings:
- REST API shows better reliability (0.34% error rate)
- Shared Memory shows potential for larger payloads
- System handles ~25 requests/second with <20ms response time for 90% of requests

## Load Testing

The project includes a comprehensive load testing setup using Locust to compare the performance of both communication methods. See the [load-testing documentation](load-testing/README.md) for details on:

- Setting up and running load tests
- Test scenarios and metrics
- Best practices for performance testing
- Customizing test parameters

To run the load tests:

1. Install Locust dependencies:
```bash
cd load-testing
pip install -r requirements.txt
```

2. Start the load test:
```bash
locust -f locustfile.py
```

3. Access the Locust web interface at http://localhost:8089

## Error Handling

- Both services include comprehensive error handling
- Logs are provided for debugging
- Shared memory files are automatically cleaned up
- HTTP errors are properly propagated

## Contributing

Feel free to submit issues and enhancement requests. 