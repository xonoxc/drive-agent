#!/bin/bash

# start the api
uv run uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} &


# start the frontend
uv run streamlit run frontend/app.py \
  --server.address=0.0.0.0 \
  --server.port=8501
