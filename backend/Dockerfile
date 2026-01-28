# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy environment file
COPY .env .env

# Copy application code
COPY src/ ./src/
COPY create_tables.py ./

# Expose port 8000
EXPOSE 8000

# Run application
CMD ["python", "-m","uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
