# gunicorn.conf.py

import os

# Application to run (pointing to your ASGI application in `asgi.py`)
# Replace `myproject` with your Django project name
import home.asgi
application = home.asgi.application

# Bind to a specific IP and port (default is 127.0.0.1:8000)
bind = "0.0.0.0:8000"

# Specify the worker class for ASGI, use Uvicorn worker
worker_class = "uvicorn.workers.UvicornWorker"

# Number of worker processes (can adjust based on your server's capacity)
workers = 4

# Timeout setting (default is 30 seconds, increase if needed)
timeout = 60

# Log level for Gunicorn logging
loglevel = "info"

# Access and error log file locations
accesslog = "-"
errorlog = "-"

# Enable automatic worker process recycling (default: no)
# max_requests = 1000
# max_requests_jitter = 50

# Daemon mode to run Gunicorn in the background (optional)
# daemon = True

# Keep these settings for the ASGI application in case you use Django Channels
# max_request_size = 1000000  # in bytes (optional)
