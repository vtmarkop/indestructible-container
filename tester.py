import requests
import time
from datetime import datetime

url = "http://127.0.0.1:8080"

# --- CHANGE 1: Create a Browser Session ---
# This object will automatically store cookies for us
client = requests.Session()

total_requests = 0
successful_requests = 0

print(f"--- Starting Stateful Monitor on {url} ---")

while True:
    try:
        total_requests += 1
        start = time.time()
        
        # --- CHANGE 2: Use client.get instead of requests.get ---
        response = client.get(url, timeout=3)
        
        duration = round((time.time() - start) * 1000)
        timestamp = datetime.now().strftime("%H:%M:%S")

        if response.status_code == 200:
            successful_requests += 1
            availability = (successful_requests / total_requests) * 100
            
            # Print the response (User ID will now stay the same!)
            print(f"[{timestamp}] ✅ 200 OK | {duration}ms | MSG: {response.text.strip()} | Availability: {availability:.2f}%")
        else:
            print(f"[{timestamp}] ⚠️ ERROR: {response.status_code}")

    except Exception as e:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] ❌ FAILED: {str(e)}")

    time.sleep(0.5)