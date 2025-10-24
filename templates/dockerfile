# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Flask app and templates explicitly
COPY app.py /app/app.py
COPY templates/ /app/templates/

# Expose the Flask default port
EXPOSE 5000

# Define the command to run the application
CMD ["python", "app.py"]