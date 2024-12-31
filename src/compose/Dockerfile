FROM python:3.12-slim

WORKDIR /app/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install pipenv
RUN pip install --upgrade pip pipenv watchfiles

# Copy Pipfile and lock file
COPY ./Pipfile* ./

# Generate and install Python dependencies
RUN pipenv requirements > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application directory
VOLUME /app/
