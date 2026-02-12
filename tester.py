import requests
import time
from datetime import datetime

# URL configuration (Default port 8080)
url = "http://127.0.0.1:8080"

total_requests = 0
successful_requests = 0

print(f"--- Starting Rolling Update Monitor on {url} ---")

while True:
    try:
        total_requests += 1
        start = time.time()
        
        # Timeout set to 3s to handle network hiccups
        response = requests.get(url, timeout=3)
        
        duration = round((time.time() - start) * 1000)
        timestamp = datetime.now().strftime("%H:%M:%S")

        if response.status_code == 200:
            successful_requests += 1
            availability = (successful_requests / total_requests) * 100
            
            # --- THE NEW PRINT LINE (Fixed Indentation) ---
            print(f"[{timestamp}] ✅ 200 OK | {duration}ms | MSG: {response.text.strip()} | Availability: {availability:.2f}%")
        else:
            print(f"[{timestamp}] ⚠️ ERROR: {response.status_code}")

    except Exception as e:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] ❌ FAILED: {str(e)}")

    time.sleep(0.5)