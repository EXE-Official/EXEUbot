# Use a base Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the configuration file and dependencies
COPY pyproject.toml poetry.lock ./

# Install FFMPEG
RUN apt update 
RUN apt upgrade
RUN apt install ffmpeg

# Install Poetry
RUN pip install --no-cache-dir poetry

# Install project dependencies
RUN poetry install --no-interaction --no-ansi

# Copy the entire project to the working directory
COPY . .

# Specify the startup command
CMD ["poetry", "run", "python", "main.py"]
