import socket
import time
import os
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics # <--- NEW

app = Flask(__name__)

# --- 📊 METRICS SETUP ---
# This automatically exposes a /metrics endpoint for Prometheus
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')
# ------------------------

@app.route('/')
def home():
    container_id = socket.gethostname()
    return f"✅ [Corrected] Response from: {container_id}\n"

@app.route('/crash')
def crash():
    # The Chaos Monkey trigger
    print("💥 CRITICAL ERROR: Committing suicide...")
    os._exit(1)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)