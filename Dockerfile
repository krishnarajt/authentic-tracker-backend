# Use a lightweight official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Prevent .pyc files and enable instant logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy dependency file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source
COPY . .

# Expose port
EXPOSE 8000

# Default command — adjust module path if your app file differs
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
