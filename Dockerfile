# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.11.6-slim-bookworm

# Set the working directory to /app
WORKDIR /app

# Install curl, wget, and unzip
RUN apt-get update && apt-get install -y curl wget unzip

# Install GnuPG
RUN apt-get update && apt-get install -y gnupg

RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    gfortran \
    python3-dev \
    build-essential

# Upgrade pip, setuptools, and wheel
RUN python3 -m pip install --upgrade pip setuptools wheel

# Install Cython and NumPy
RUN pip3 install cython numpy
RUN pip3 install requests==2.26.0
RUN pip3 install selenium==4.13.0
RUN pip3 install dnspython==2.2.0
RUN pip3 install pandas

# Install application requirements
# COPY requirements.txt .
# RUN pip3 install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app
