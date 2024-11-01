FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Make Python 3.10 the default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Install poetry
ENV POETRY_VERSION=1.4.2
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Configure poetry
RUN poetry config virtualenvs.create false

# set working directory
WORKDIR /app

# Copy only pyproject.toml first to cache dependencies
COPY pyproject.toml ./

# Generate poetry.lock and install dependencies
RUN poetry lock && poetry install --no-root

# Copy the rest of the application
COPY counter_app counter_app/

# Install the root package
RUN poetry install

# Listen to port 5000 at runtime
EXPOSE 5000

# Define our command to be run when launching the container
CMD poetry run gunicorn counter_app.wsgi:app -b 0.0.0.0:5001  --reload
