# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn

# RUN python3 pre_downloads.py


ENV HOST="0.0.0.0"
ENV PORT=8000
ENTRYPOINT uvicorn app.app:app --host ${HOST} --port ${PORT}
