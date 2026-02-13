import socket
import os
import redis
import uuid
from flask import Flask, request, make_response
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# --- 🧠 DATABASE CONNECTION ---
# Connect to Redis
cache = redis.Redis(host='redis', port=6379, decode_responses=True)

# --- 📊 METRICS ---
metrics = PrometheusMetrics(app)

@app.route('/')
def home():
    container_id = socket.gethostname()
    
    # --- 1. IDENTIFY THE USER ---
    # Check if they brought their "ID Card" (Cookie)
    session_token = request.cookies.get('session_token')
    
    if not session_token:
        # New User: Give them a brand new ID
        session_token = str(uuid.uuid4())
        is_new = True
    else:
        # Returning User: We know them!
        is_new = False

    # --- 2. UPDATE REDIS ( The "State" ) ---
    
    # A. The Global Counter (Shared by everyone)
    global_hits = cache.incr('total_hits')
    
    # B. The Personal Counter (Specific to THIS user)
    # We create a unique key just for them: "user:UUID:hits"
    user_key = f"user:{session_token}:hits"
    user_hits = cache.incr(user_key)
    
    # Optional: Set their data to expire in 1 hour so Redis doesn't fill up forever
    cache.expire(user_key, 3600)

    # --- 3. BUILD RESPONSE ---
    response_text = (
        f"🖥️  Serving Container: {container_id}\n"
        f"👤 Your ID: {session_token}\n"
        f"🌍 Global System Hits: {global_hits}\n"
        f"👉 YOUR Personal Hits: {user_hits}\n"
    )
    
    response = make_response(response_text)
    
    # Secure the ID card on the user's browser
    if is_new:
        response.set_cookie('session_token', session_token)
        
    return response

@app.route('/crash')
def crash():
    os._exit(1)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)