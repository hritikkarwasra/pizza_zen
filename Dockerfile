# Use an official Python runtime as a parent image
FROM python:3.9.2

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /pizza_zen

# Install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Install the necessary MySQL client library dependencies
RUN apt-get update && apt-get install -y default-libmysqlclient-dev

# Install MySQLdb with support for caching_sha2_password
RUN pip install mysqlclient

# Copy the project code into the container
COPY . /pizza_zen