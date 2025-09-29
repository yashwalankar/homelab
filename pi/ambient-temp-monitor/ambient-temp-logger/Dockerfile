# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY app/ .

# Run the app by default
CMD ["python", "app.py"]

# for testing CMD ["python","-u" "app.py"]