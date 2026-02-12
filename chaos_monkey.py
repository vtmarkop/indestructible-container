import time
import random
import subprocess
import datetime

# --- 🛡️ BACKUP CONFIGURATION ---
BACKUP_TARGETS = [
    "indestructible-container-app1-1", 
    "indestructible-container-app2-1"
]
# -------------------------------

def log(message):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🐵 {message}")

def get_targets():
    """
    Returns the list of targets and the mode name.
    """
    mode = "UNKNOWN"
    targets = []
    
    try:
        # 1. Try Auto-Discovery
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"], 
            capture_output=True, text=True
        )
        
        # Filter for 'app' and clean names
        found = [line.strip() for line in result.stdout.splitlines() if "app" in line.lower()]
        
        if found:
            targets = found
            mode = "AUTO"
        else:
            # Found nothing? Switch to backup.
            targets = BACKUP_TARGETS
            mode = "BACKUP (Auto returned 0)"
            
    except Exception as e:
        # Error? Switch to backup.
        targets = BACKUP_TARGETS
        mode = f"BACKUP (Error: {e})"
    
    return targets, mode

def inject_suicide(victim):
    # The 'Internal Suicide' command
    cmd = [
        "docker", "exec", victim, 
        "python", "-c", 
        "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/crash')"
    ]

    try:
        # We expect a timeout because the container dies instantly
        subprocess.run(cmd, timeout=5, capture_output=True)
        log(f"💥 BOOM! {victim} terminated.")
    except subprocess.TimeoutExpired:
        log(f"💥 BOOM! {victim} died instantly.")
    except Exception:
        log(f"💥 Attack sent to {victim}.")

print("--- 🐵 TRANSPARENT CHAOS MONKEY STARTED ---")

while True:
    # 1. Get Targets and Mode
    current_targets, current_mode = get_targets()
    
    # 2. Log the Status (So you know what's happening)
    log(f"Mode: [{current_mode}] | Targets found: {len(current_targets)}")
    
    if not current_targets:
        log("❌ CRITICAL: No targets found. Retrying in 5s...")
        time.sleep(5)
        continue

    # 3. Pick a victim
    victim = random.choice(current_targets)
    log(f"🎯 Target Locked: {victim}")

    # 4. Attack!
    inject_suicide(victim)

    # 5. Sleep (And tell you about it)
    sleep_time = 20
    log(f"💤 Sleeping for {sleep_time}s to allow recovery...")
    time.sleep(sleep_time)