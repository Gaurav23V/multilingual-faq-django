# Use the official Python image as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose port 8000 for the Django app
EXPOSE 8000

# Define the default command to run when starting the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]