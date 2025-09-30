FROM python:3.12-slim

WORKDIR /app

# Install system dependencies needed by psycopg2-binary or other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    bash \
    dos2unix \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Convert entrypoint to Unix line endings (fix CRLF issues when building on Windows)
RUN if [ -f /app/scripts/entrypoint.sh ]; then dos2unix /app/scripts/entrypoint.sh || true; fi

# Make entrypoint executable
RUN chmod +x /app/scripts/entrypoint.sh

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
