# Use the official Python base image
FROM python:3.12-slim

# Set environment variables to prevent .pyc files and use unbuffered I/O
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and .env into the container
COPY requirements.txt /app/
COPY .env /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app directory into the container
COPY app /app/app

# Expose the Flask app's default port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app/main.py"]
