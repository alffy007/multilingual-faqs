# Use an official Python runtime as a parent image
FROM python:3.11.7-slim-bullseye


ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

ADD . /app

# Install dependencies
COPY requirements.txt /app

RUN pip install  -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port the app runs on
EXPOSE 80

EXPOSE 5432
# Run the application
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:80"]
