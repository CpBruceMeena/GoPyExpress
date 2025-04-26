# Load Testing Setup

This directory contains the load testing configuration for the Go-Python API project using Locust.

## Prerequisites

- Python 3.7 or higher
- Locust 2.20.1 or higher

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure both the Go and Python services are running:
```bash
# Terminal 1 - Python API
cd ../python-api
python main.py

# Terminal 2 - Go API
cd ../golang-api
go run main.go
```

## Running Load Tests

1. Start Locust with the default configuration:
```bash
locust -f locustfile.py
```

2. Open your browser and navigate to:
```
http://localhost:8089
```

3. Configure the test:
   - Number of users: Start with 10
   - Spawn rate: 1 user/second
   - Host: http://localhost:8080 (Go API)

4. Start the test and monitor the results

## Test Scenarios

The load test includes two main scenarios:

1. **Direct API Call** (`/api/users-via-api`)
   - Tests the performance of direct HTTP API calls
   - Measures response time and success rate

2. **Shared Memory** (`/api/users-via-shm`)
   - Tests the performance of shared memory communication
   - Measures response time and success rate

## Metrics Tracked

- Response time
- Requests per second
- Number of failures
- Response size
- Error rates

## Customizing Tests

You can modify the `locustfile.py` to:
- Change the wait time between requests
- Add more test scenarios
- Modify the payload size
- Add more complex test cases

## Best Practices

1. Start with a small number of users and gradually increase
2. Monitor system resources during tests
3. Run tests for at least 5 minutes to get stable results
4. Compare results between different payload sizes
5. Document any errors or failures for analysis 