FROM python:3.10-slim

WORKDIR /app

# Dependencias necesarias para OpenCV + mosquitto-clients
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    mosquitto-clients \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt || true

COPY src/ ./src/
COPY config.yaml /app/config.yaml

CMD ["python", "src/main.py"]