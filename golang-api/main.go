package main

import (
	"encoding/binary"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

const (
	SHM_DIR  = "shared_memory"
	SHM_NAME = "users_shm"
	SHM_SIZE = 1024
)

type User struct {
	ID        int    `json:"id"`
	FirstName string `json:"first_name"`
	LastName  string `json:"last_name"`
	Email     string `json:"email"`
	Age       int    `json:"age"`
}

func getShmPath() string {
	// Use the system temp directory
	tmpDir := os.TempDir()
	shmDir := filepath.Join(tmpDir, SHM_DIR)

	// Create the shared memory directory if it doesn't exist
	if err := os.MkdirAll(shmDir, 0755); err != nil {
		log.Printf("Warning: Could not create shared memory directory: %v", err)
	}

	shmPath := filepath.Join(shmDir, SHM_NAME)
	log.Printf("Using shared memory file: %s", shmPath)
	return shmPath
}

func getUsersViaAPI() ([]map[string]interface{}, error) {
	startTime := time.Now()
	log.Printf("Starting API request to Python service")

	resp, err := http.Get("http://localhost:5000/api/users")
	if err != nil {
		return nil, fmt.Errorf("failed to make API request: %v", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response body: %v", err)
	}

	var users []map[string]interface{}
	if err := json.Unmarshal(body, &users); err != nil {
		return nil, fmt.Errorf("failed to parse response: %v", err)
	}

	log.Printf("API request completed in %v", time.Since(startTime))
	return users, nil
}

func readFromSharedMemory() ([]map[string]interface{}, error) {
	startTime := time.Now()
	log.Printf("Starting shared memory read")

	shmPath := getShmPath()

	// Open memory-mapped file
	file, err := os.OpenFile(shmPath, os.O_RDONLY, 0666)
	if err != nil {
		return nil, fmt.Errorf("failed to open shared memory file: %v", err)
	}
	defer file.Close()

	// Read the size
	var size uint32
	if err := binary.Read(file, binary.BigEndian, &size); err != nil {
		return nil, fmt.Errorf("failed to read size: %v", err)
	}

	// Read the data
	data := make([]byte, size)
	if _, err := file.Read(data); err != nil {
		return nil, fmt.Errorf("failed to read data: %v", err)
	}

	// Parse JSON data
	var users []map[string]interface{}
	if err := json.Unmarshal(data, &users); err != nil {
		return nil, fmt.Errorf("failed to parse data: %v", err)
	}

	// Clean up the shared memory file
	if err := os.Remove(shmPath); err != nil {
		log.Printf("Warning: Failed to remove shared memory file: %v", err)
	}

	log.Printf("Shared memory read completed in %v", time.Since(startTime))
	return users, nil
}

func handleUsersViaAPI(w http.ResponseWriter, r *http.Request) {
	log.Printf("Received request for /api/users-via-api")
	startTime := time.Now()

	users, err := getUsersViaAPI()
	if err != nil {
		log.Printf("Error: %v", err)
		http.Error(w, fmt.Sprintf("Error getting users via API: %v", err), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(users); err != nil {
		log.Printf("Error encoding response: %v", err)
		http.Error(w, "Error encoding response", http.StatusInternalServerError)
		return
	}

	log.Printf("Total request time via API: %v", time.Since(startTime))
}

func handleUsersViaSharedMemory(w http.ResponseWriter, r *http.Request) {
	log.Printf("Received request for /api/users-via-shm")
	startTime := time.Now()

	// Request Python to write data to shared memory
	resp, err := http.Get("http://localhost:5000/api/write-to-shm")
	if err != nil {
		log.Printf("Error requesting Python to write data: %v", err)
		http.Error(w, fmt.Sprintf("Error requesting data write: %v", err), http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		log.Printf("Python service returned error: %v", resp.Status)
		http.Error(w, "Python service failed to write data", http.StatusInternalServerError)
		return
	}

	// Read from shared memory
	users, err := readFromSharedMemory()
	if err != nil {
		log.Printf("Error: %v", err)
		http.Error(w, fmt.Sprintf("Error reading from shared memory: %v", err), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(users); err != nil {
		log.Printf("Error encoding response: %v", err)
		http.Error(w, "Error encoding response", http.StatusInternalServerError)
		return
	}

	log.Printf("Total request time via shared memory: %v", time.Since(startTime))
}

func main() {
	// Register routes
	http.HandleFunc("/api/users-via-api", handleUsersViaAPI)
	http.HandleFunc("/api/users-via-shm", handleUsersViaSharedMemory)

	// Start server
	port := ":8080"
	log.Printf("Starting server on port %s", port)
	log.Fatal(http.ListenAndServe(port, nil))
}
