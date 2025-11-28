FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Environment variable for Flask
ENV FLASK_APP=app.py

# Expose the same port your app listens on
EXPOSE 80

# Run the app
CMD ["python", "app.py"]

