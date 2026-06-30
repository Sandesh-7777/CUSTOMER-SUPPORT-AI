#!/bin/bash

echo "Rebuilding vector store from PDFs..."

python3 rag/ingest.py

echo "Starting server..."

uvicorn main:app --host 0.0.0.0 --port $PORT