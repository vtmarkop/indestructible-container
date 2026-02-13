FROM python:3.9-slim

# --- 🛠️ INSTALL NETWORK TOOLS ---
# We need 'iproute2' to use the 'tc' command for chaos
RUN apt-get update && apt-get install -y iproute2 iputils-ping && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY server.py .
CMD ["python", "server.py"]