#!/bin/bash

# start the api
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 &


# start the frontend
uv run streamlit run frontend/app.py \
  --server.address=0.0.0.0 \
  --server.port=8501
