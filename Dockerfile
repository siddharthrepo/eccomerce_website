# Use official Python runtime as base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Change to the Django project directory
WORKDIR /app/ecommerce

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Create directory for media files
RUN mkdir -p /app/ecommerce/media

# Expose port 8000
EXPOSE 8000

# Run migrations and start Gunicorn server
CMD python manage.py migrate && \
    gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
