import mmap
import os
import json
import time
import struct
import tempfile
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Configuration
SHM_DIR = os.path.join(tempfile.gettempdir(), "shared_memory")
SHM_NAME = os.path.join(SHM_DIR, "users_shm")
SHM_SIZE = 2 * 1024 * 1024  # Increased to 2MB to accommodate larger payload

def ensure_shm_directory():
    """Ensure the shared memory directory exists"""
    if not os.path.exists(SHM_DIR):
        os.makedirs(SHM_DIR, exist_ok=True)
        print(f"Created shared memory directory at {SHM_DIR}")

def get_user_data():
    # Generate 100 users with more detailed information
    users = []
    for i in range(1, 101):
        user = {
            "id": i,
            "first_name": f"User{i}",
            "last_name": f"LastName{i}",
            "email": f"user{i}@example.com",
            "age": 20 + (i % 50),  # Age between 20-69
            "address": {
                "street": f"{i} Main Street",
                "city": "Sample City",
                "state": "Sample State",
                "zip": f"123{i:02d}",
                "country": "Sample Country",
                "coordinates": {
                    "latitude": 37.7749 + (i * 0.0001),
                    "longitude": -122.4194 + (i * 0.0001)
                }
            },
            "phone": f"+1-555-{i:03d}-{i:04d}",
            "interests": [
                "Reading",
                "Programming",
                "Hiking",
                "Cooking",
                "Photography",
                "Traveling",
                "Music",
                "Sports",
                "Movies",
                "Gaming"
            ],
            "education": {
                "degree": "Bachelor's",
                "major": "Computer Science",
                "university": "Sample University",
                "graduation_year": 2010 + (i % 10),
                "gpa": 3.5 + (i % 5) * 0.1,
                "courses": [
                    "Data Structures",
                    "Algorithms",
                    "Database Systems",
                    "Operating Systems",
                    "Computer Networks",
                    "Software Engineering",
                    "Artificial Intelligence",
                    "Machine Learning"
                ]
            },
            "work_experience": [
                {
                    "company": f"Company {i}",
                    "position": "Software Engineer",
                    "years": 2 + (i % 5),
                    "responsibilities": [
                        "Developing and maintaining web applications",
                        "Implementing new features and functionality",
                        "Code review and quality assurance",
                        "Performance optimization",
                        "Team collaboration and mentoring"
                    ],
                    "technologies": [
                        "Python",
                        "Go",
                        "JavaScript",
                        "React",
                        "Docker",
                        "Kubernetes",
                        "AWS",
                        "PostgreSQL"
                    ]
                },
                {
                    "company": f"Previous Company {i}",
                    "position": "Junior Developer",
                    "years": 1 + (i % 3),
                    "responsibilities": [
                        "Assisting in development tasks",
                        "Bug fixing",
                        "Documentation",
                        "Testing"
                    ],
                    "technologies": [
                        "Python",
                        "JavaScript",
                        "HTML/CSS",
                        "Git"
                    ]
                }
            ],
            "skills": [
                "Python",
                "Go",
                "JavaScript",
                "SQL",
                "Docker",
                "Kubernetes",
                "AWS",
                "Git",
                "React",
                "Node.js",
                "MongoDB",
                "Redis",
                "RabbitMQ",
                "Terraform",
                "CI/CD",
                "Microservices"
            ],
            "created_at": "2024-01-01T00:00:00Z",
            "last_login": "2024-04-01T00:00:00Z",
            "is_active": True,
            "preferences": {
                "theme": "dark",
                "notifications": True,
                "language": "en",
                "timezone": "UTC",
                "email_frequency": "daily",
                "display_mode": "compact",
                "font_size": "medium",
                "color_scheme": "blue"
            },
            "social_media": {
                "twitter": f"@user{i}",
                "linkedin": f"linkedin.com/in/user{i}",
                "github": f"github.com/user{i}"
            },
            "achievements": [
                {
                    "title": "Employee of the Month",
                    "date": "2024-03-01",
                    "description": "Recognized for outstanding performance and contribution to the team"
                },
                {
                    "title": "Best Project Award",
                    "date": "2024-02-15",
                    "description": "Awarded for developing an innovative solution that improved system performance by 40%"
                }
            ],
            "projects": [
                {
                    "name": f"Project {i}",
                    "description": "A comprehensive web application for managing user data and analytics",
                    "technologies": ["Python", "React", "PostgreSQL", "Docker"],
                    "role": "Lead Developer",
                    "duration": "6 months"
                }
            ]
        }
        users.append(user)
    return users

class UserHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/users':
            try:
                users = get_user_data()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(users).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        elif self.path == '/api/write-to-shm':
            try:
                success = write_to_shared_memory()
                if success:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success"}).encode())
                else:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Failed to write to shared memory"}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

def write_to_shared_memory():
    """Write user data to shared memory file"""
    try:
        # Ensure the shared memory directory exists
        os.makedirs(SHM_DIR, exist_ok=True)
        
        # Get the full path to the shared memory file
        shm_path = os.path.join(SHM_DIR, SHM_NAME)
        
        # Remove the file if it exists to ensure fresh data
        if os.path.exists(shm_path):
            os.remove(shm_path)
        
        # Get user data
        users = get_user_data()
        
        # Convert to JSON
        json_data = json.dumps(users)
        
        # Write to shared memory file
        with open(shm_path, 'wb') as f:
            # Write size as 4-byte big-endian integer
            f.write(len(json_data).to_bytes(4, byteorder='big'))
            # Write the actual data
            f.write(json_data.encode())
        
        print(f"Successfully wrote {len(users)} users to shared memory")
        return True
    except Exception as e:
        print(f"Error writing to shared memory: {e}")
        return False

def main():
    # Ensure shared memory directory exists
    ensure_shm_directory()
    print(f"Using shared memory directory: {SHM_DIR}")
    
    # Start HTTP server in a separate thread
    server = HTTPServer(('', 5000), UserHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print('Starting server on port 5000...')
    
    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()
        server.server_close()

if __name__ == '__main__':
    main() 