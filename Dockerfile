# Use Python base image
FROM python:3.10-slim

COPY . .

# Install ffmpeg and other dependencies
RUN apt-get update && \
  apt-get install -y ffmpeg git && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# Default entrypoint
ENTRYPOINT ["flask", "--app", "main", "run"]