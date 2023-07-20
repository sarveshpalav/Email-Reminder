# Use the official Python image as the base image
FROM python:3.9-slim


# creates a new user named worker inside the Docker image. 
RUN adduser worker
#sets the working directory inside the Docker image to /home/worker/app
WORKDIR /home/worker/app
#This instruction switches the user to worker
USER worker


# Install Poetry
RUN pip install --user --no-cache-dir --upgrade pip poetry
ENV PATH=$PATH:/home/worker/.local/bin

#Copy files and directories from the host machine into the Docker image's file system
COPY --chown=worker server/ ./


# Install project dependencies
RUN poetry config virtualenvs.create true && poetry install --no-interaction --no-ansi


# Expose the port that Uvicorn will run on (change if needed)
EXPOSE 8000

#Instruction in a Dockerfile sets the working directory inside the Docker image to /home/worker/app
WORKDIR /home/worker/app


# Command to run the Uvicorn server
CMD poetry run uvicorn --host=0.0.0.0 main:app --port 8000