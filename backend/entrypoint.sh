#!/bin/sh

echo "Applying database migrations..."
alembic upgrade head

echo "Starting Gunicorn server with Uvicorn workers..."
exec gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 app.main:app