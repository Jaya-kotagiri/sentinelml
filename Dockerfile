# 1. Use a slim, stable base
FROM python:3.10-slim

# 2. Set environment variables for Python performance
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 3. Security: Create a non-privileged user
RUN groupadd -r sentineluser && useradd -r -g sentineluser sentineluser

# 4. Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy only the necessary application files
COPY ./app ./app
COPY ./models ./models
COPY ./data/processed/X_test.csv ./data/processed/X_test.csv
COPY ./data/processed/y_test.csv ./data/processed/y_test.csv

# 7. Security: Grant ownership to the non-root user
RUN chown -R sentineluser:sentineluser /app
USER sentineluser

# 8. Define a Healthcheck
# This tells the orchestrator (like Docker Compose) if the API is actually "alive"
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/docs || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]