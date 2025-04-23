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
SHM_SIZE = 1024  # Size in bytes

def ensure_shm_directory():
    """Ensure the shared memory directory exists"""
    if not os.path.exists(SHM_DIR):
        os.makedirs(SHM_DIR, exist_ok=True)
        print(f"Created shared memory directory at {SHM_DIR}")

def get_user_data():
    return [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "age": 30
        },
        {
            "id": 2,
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "age": 28
        }
    ]

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