# Load Testing Results

## Test Configuration

- **Duration**: 2 minutes
- **Number of Users**: 50
- **Spawn Rate**: 10 users/second
- **Payload Size**: ~251 KB (256,873 bytes)
- **Test Environment**: Local machine
- **Test Date**: April 26, 2024

## Test Scenarios

1. **REST API Endpoint** (`/api/users-via-api`)
   - Direct HTTP communication between Go and Python services
   - Data transfer via HTTP/JSON

2. **Shared Memory Endpoint** (`/api/users-via-shm`)
   - Communication via shared memory
   - HTTP signaling for coordination

## Performance Metrics

### Throughput

| Endpoint | Requests/sec | Total Requests |
|----------|--------------|----------------|
| REST API | 12.39 | 1,471 |
| Shared Memory | 12.26 | 1,455 |
| **Total** | **24.65** | **2,926** |

### Response Times (in milliseconds)

| Metric | REST API | Shared Memory |
|--------|----------|---------------|
| Average | 13 | 14 |
| Median | 10 | 11 |
| 90th percentile | 18 | 19 |
| 95th percentile | 26 | 27 |
| Maximum | 163 | 202 |

### Error Rates

| Endpoint | Total Requests | Failures | Failure Rate |
|----------|----------------|----------|--------------|
| REST API | 1,471 | 5 | 0.34% |
| Shared Memory | 1,455 | 70 | 4.81% |
| **Total** | **2,926** | **75** | **2.56%** |

## Detailed Analysis

### REST API Performance
- **Strengths**:
  - Lower error rate (0.34%)
  - More consistent response times
  - Better stability under load
  - Simpler implementation
- **Weaknesses**:
  - Slightly higher overhead due to HTTP protocol
  - Network dependency

### Shared Memory Performance
- **Strengths**:
  - Direct memory access
  - No network protocol overhead
  - Potential for better performance with larger payloads
- **Weaknesses**:
  - Higher error rate (4.81%)
  - More complex implementation
  - Requires careful resource management

## Response Time Distribution

### REST API
- 50% of requests: ≤ 10ms
- 75% of requests: ≤ 13ms
- 90% of requests: ≤ 18ms
- 95% of requests: ≤ 26ms
- 99% of requests: ≤ 78ms

### Shared Memory
- 50% of requests: ≤ 11ms
- 75% of requests: ≤ 14ms
- 90% of requests: ≤ 19ms
- 95% of requests: ≤ 27ms
- 99% of requests: ≤ 82ms

## Recommendations

1. **For Current Payload Size (~251 KB)**:
   - REST API is recommended due to:
     - Lower error rate
     - More consistent performance
     - Better stability
     - Simpler maintenance

2. **Potential Optimizations**:
   - Shared Memory:
     - Investigate and fix error causes
     - Implement better error handling
     - Optimize resource cleanup
   - REST API:
     - Consider connection pooling
     - Implement caching if applicable

3. **Future Testing**:
   - Test with different payload sizes
   - Test with higher concurrency
   - Test with different data patterns
   - Test with different hardware configurations

## Conclusion

For the current implementation and payload size, the REST API approach provides better reliability and consistency. However, the shared memory approach shows potential for better performance with larger payloads or different use cases.

The system can handle approximately 25 requests per second with response times under 20ms for 90% of requests, which is suitable for many use cases. The error rates, while higher for shared memory, are still within acceptable ranges for most applications.

## Next Steps

1. Investigate the causes of shared memory errors
2. Run tests with different payload sizes
3. Test with higher concurrency levels
4. Implement suggested optimizations
5. Consider hybrid approach for different use cases 