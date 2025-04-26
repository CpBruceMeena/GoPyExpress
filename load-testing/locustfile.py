from locust import HttpUser, task, between
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIUser(HttpUser):
    wait_time = between(1, 3)  # Wait between 1 and 3 seconds between tasks
    
    def on_start(self):
        """Initialize test data"""
        self.test_data = {
            "payload_size": "small",  # or "large"
            "test_type": "api"  # or "shm"
        }
    
    @task(1)
    def test_api_endpoint(self):
        """Test the direct API endpoint"""
        self.test_data["test_type"] = "api"
        self._make_request("/api/users-via-api")
    
    @task(1)
    def test_shm_endpoint(self):
        """Test the shared memory endpoint"""
        self.test_data["test_type"] = "shm"
        self._make_request("/api/users-via-shm")
    
    def _make_request(self, endpoint):
        """Make HTTP request and log results"""
        with self.client.get(
            endpoint,
            name=f"{endpoint} [{self.test_data['payload_size']}]",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    response_length = len(json.dumps(data))
                    logger.info(
                        f"Endpoint: {endpoint}, "
                        f"Status: {response.status_code}, "
                        f"Response Time: {response.elapsed.total_seconds():.3f}s, "
                        f"Response Size: {response_length} bytes"
                    )
                except json.JSONDecodeError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Status code: {response.status_code}")
    
    def on_stop(self):
        """Cleanup after test"""
        logger.info("Test completed") 