FROM python:3.13

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    python3-venv \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Create the virtual environment
RUN python -m venv venv

# Install dependencies from requirements.txt
COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . /app

# Expose the application port
EXPOSE 8000

# Ensure we use the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Run the application inside the virtual environmen
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

