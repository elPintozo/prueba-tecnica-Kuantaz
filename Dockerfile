FROM python:3.10.0-slim-buster

WORKDIR /app

RUN apt-get update \
    && apt-get install -y libpq-dev \
    && apt-get install -y postgresql-client

# Install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=development
ENV DATABASE_URL=postgresql://postgres:postgres@db:5432/kuantaz_db

# Expose port
EXPOSE 5001

# Start the application
CMD ["python", "app.py"]