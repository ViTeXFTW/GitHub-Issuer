# Dockerfile

# Stage 1: Builder
FROM python:3-alpine AS builder

WORKDIR /app

# Create a virtual environment
RUN python3 -m venv venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Stage 2: Runner
FROM python:3-alpine AS runner

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/venv venv

# Copy the bot.py file and any other necessary files
COPY bot.py bot.py

# Set environment variables
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Expose the port for Flask
EXPOSE 8000

# Command to run the bot
CMD ["python", "bot.py"]