# Use official Python image as the base image
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Add a working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY . /app

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt