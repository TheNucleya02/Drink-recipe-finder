# Use Python 3.11 Slim (Lightweight)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for PostgreSQL)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Copy the rest of the code
COPY . /app/


# Run Gunicorn
# 'drink_recipes' matches your project name in settings.py
CMD sh -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn drink_recipes.wsgi:application --bind 0.0.0.0:8000"
