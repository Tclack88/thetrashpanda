# Use Debian-based Python base image
FROM python:3.8.0-slim-buster

# Install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    # OpenCV dependencies
    apt-get install -y libglib2.0-0 libsm6 libxext6 && \
    apt-get install -y libglib2.0-0 libxrender1 libfontconfig1 && \
    # Pillow dependencies
    apt-get install -y libjpeg-dev zlib1g-dev && \
    apt-get clean

# Set envirovars
# Prevent pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents buffering stdout and sdterr
ENV PYTHONUNBUFFERED 1

# Create + set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Add and install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# Add app
COPY . /usr/src/app

# Run the Flask dev server
CMD python manage.py run -h 0.0.0.0
