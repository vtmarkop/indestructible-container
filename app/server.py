from flask import Flask
import os           # <--- NEW: Needed for self-destruction
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    container_id = socket.gethostname()
    return f"🚀 VERSION 2.0! Server: {container_id}\n", 200

# --- THE CHAOS ENDPOINT ---
@app.route('/crash')
def crash():
    # Force the process to exit immediately with an error code
    # This simulates a fatal application crash.
    os._exit(1)  

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)