# Use a Python base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file to the container
COPY pyproject.toml poetry.lock /app/

# Install Poetry and project dependencies
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the project directory to the container
COPY . /app/

# Expose the port your app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "pitch_health_monitor.main:app", "--host", "0.0.0.0", "--port", "8000"]