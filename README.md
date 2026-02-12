\# 🛡️ Indestructible Container Architecture



> \*\*A Chaos Engineering Proof-of-Concept\*\*

> \*Achieving Zero-Downtime \& Self-Healing with Docker, NGINX, and Python.\*



\[Image of high availability architecture diagram]



\## 📖 Overview



This project demonstrates a production-grade \*\*Resilient Architecture\*\* capable of surviving random server failures ("Chaos") and performing software updates ("Evolution") without a single second of downtime for the user.



It simulates a real-world environment where a \*\*Chaos Monkey\*\* script randomly kills backend servers, forcing the system to self-heal while maintaining 100% availability.



\## 🏗️ Architecture



The system is built on the \*\*"Redundant Load Balancer"\*\* pattern:



\* \*\*Gatekeeper (NGINX):\*\* A reverse proxy that distributes traffic and instantly detects failures.

\* \*\*The Fleet (Flask Apps):\*\* Two identical Python web servers (`instance-01`, `instance-02`).

\* \*\*The Supervisor (Docker Compose):\*\* Enforces a `restart: always` policy to resurrect dead containers.

\* \*\*The Chaos Monkey:\*\* A Python bot that randomly terminates containers to test resilience.



---



\## 🚀 Quick Start



\### Prerequisites

\* \[Docker Desktop](https://www.docker.com/products/docker-desktop)

\* Python 3.x



\### 1. Start the Infrastructure

Launch the cluster in detached mode. This builds the images and starts NGINX + 2 App containers.

```bash

docker-compose up -d --build

