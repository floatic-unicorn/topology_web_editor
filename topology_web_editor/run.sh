#!/bin/bash

# Function to handle cleanup on exit
cleanup() {
  echo "Cleaning up..."
  # Kill the background processes
  kill -s SIGTERM $http_server_pid $flask_app_pid
  exit 0
}

# Trap Ctrl+C to call the cleanup function
trap cleanup INT

# Run the Flask app
cd backend
python3 app.py &
flask_app_pid=$!
cd ..

# Run the HTTP server
cd frontend
python3 -m http.server --bind 127.0.0.1 &
http_server_pid=$!

# Wait for the background processes to finish
wait $flask_app_pid $http_server_pid || true