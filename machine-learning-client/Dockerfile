# Base image
FROM python:3.8-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the Python script into the container
COPY MLClient.py /app/MLClient.py

# Install required Python packages
RUN pip install opencv-python-headless pymongo

# Run the script
CMD ["python", "MLClient.py"]
