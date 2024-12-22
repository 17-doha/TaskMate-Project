# Use the official Python image as the base image
FROM python:3.12-slim


# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY ./taskmate /app/taskmate

WORKDIR /app/taskmate


# Expose the port Django runs on
EXPOSE 8000

# Collect static files
# RUN python manage.py collectstatic --noinput

# Run migrations and start the Django development server
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && daphne -b 0.0.0.0 -p 8000 taskmate.asgi:application"]

