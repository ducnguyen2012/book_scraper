#!/bin/bash

echo "Running main..."

cd api/
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

# Lấy PID của API server
API_PID=$!

# Quay về thư mục gốc
cd ..

echo "API server started with PID $API_PID"

echo "Waiting for API to start..."
sleep 5

echo "Running rpa..."

cd rpa/
python3 bot.py

# Sau khi RPA chạy xong, kill API server
echo "Stopping API server..."
kill $API_PID

echo "Done."