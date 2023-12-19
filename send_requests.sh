#!/bin/bash

# Endpoint URL
url="http://127.0.0.1:5000/file"

# Number of requests to send
num_requests=100

# Loop to send requests
for i in $(seq 1 $num_requests); do
    # Generate some unique content for each request
    content="This is test content $i"

    # Send a POST request with curl
    curl -X POST "$url" -H "Content-Type: application/json" -d "{\"filename\":\"testfile$i.txt\", \"content\":\"$content\"}"

    echo " - Request $i sent"
done

echo "All requests sent."
