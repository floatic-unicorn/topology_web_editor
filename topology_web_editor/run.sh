#!/bin/bash
python3 backend/app.py &

cd frontend
python3 -m http.server --bind 127.0.0.1