FROM python:3.13.3-slim

LABEL maintainer="autumn.dawn.hope@gmail.com"
# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY . /app/

# Install the dependencies
RUN apt-get update && apt-get install -y pipx

RUN pipx install uv

RUN pipx ensurepath

RUN source /root/.bashrc

RUN uv venv

RUN uv sync

# Expose the port the app runs on
EXPOSE 8000

# Create a volume for the database
VOLUME ["/app/db"]

# Run the application
CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]