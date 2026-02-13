import time
import random
import subprocess
import datetime

def log(message):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🎲 {message}")

def get_victim():
    result = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
    targets = [line.strip() for line in result.stdout.splitlines() if "app" in line]
    return random.choice(targets) if targets else None

def inject_loss(container, percent=20):
    # 1. Drop 50% of packets randomly
    cmd = f"docker exec {container} tc qdisc add dev eth0 root netem loss {percent}%"
    subprocess.run(cmd.split())
    log(f"💔 INJECTED: {container} is losing {percent}% of packets!")

def heal(container):
    cmd = f"docker exec {container} tc qdisc del dev eth0 root"
    subprocess.run(cmd.split(), stderr=subprocess.DEVNULL)
    log(f"❤️ HEALED: {container} connection restored.")

print("--- 🎲 PACKET LOSS CHAOS STARTED ---")
print("    (Simulating 20% packet drops)")

while True:
    victim = get_victim()
    if not victim:
        log("No targets found..."); time.sleep(5); continue

    inject_loss(victim)
    time.sleep(15)
    heal(victim)
    
    log("💤 Cooling down for 10s...")
    time.sleep(10)