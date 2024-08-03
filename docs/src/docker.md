# Docker Documentation

## Overview

This document provides an overview of how to use Docker for containerizing your application.

## Dockerfile

Here is an example `Dockerfile` for a Python application:

```dockerfile
# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port on which the app will run
EXPOSE 8000

# Define the command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
