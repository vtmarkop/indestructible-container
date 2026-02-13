import time
import random
import subprocess
import datetime

def log(message):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🐌 {message}")

def get_victim():
    # Find running app containers
    result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
    targets = [line.strip() for line in result.stdout.splitlines() if "app" in line]
    return random.choice(targets) if targets else None

def inject_latency(container, delay_ms=3000):
    # 1. Add 3000ms delay to all outgoing traffic
    cmd = f"docker exec {container} tc qdisc add dev eth0 root netem delay {delay_ms}ms"
    subprocess.run(cmd.split())
    log(f"🔴 INJECTED: {container} is now lagging by {delay_ms}ms!")

def heal(container):
    # 2. Remove the rule (Restore normal speed)
    cmd = f"docker exec {container} tc qdisc del dev eth0 root"
    # We ignore errors in case it was already healed
    subprocess.run(cmd.split(), stderr=subprocess.DEVNULL)
    log(f"🟢 HEALED: {container} is fast again.")

print("--- 🐌 HIGH LATENCY CHAOS STARTED ---")
print("    (Simulating 3000ms network lag)")

while True:
    victim = get_victim()
    if not victim:
        log("No targets found. Retrying..."); time.sleep(5); continue

    # Attack
    inject_latency(victim)
    
    # Hold the chaos for 15 seconds
    time.sleep(15)
    
    # Heal
    heal(victim)
    
    # Wait before next attack
    log("💤 Cooling down for 10s...")
    time.sleep(10)