FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install only what your stack requires (NO MySQL system deps needed)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies first for Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose internal port
EXPOSE 8000

# Good practice for FastAPI in production
ENV PYTHONUNBUFFERED=1

# Run Uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
