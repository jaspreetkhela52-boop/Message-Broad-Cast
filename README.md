# 📡 Python LAN Broadcast System

Send messages from one server to 100 clients over local network.

---

## Files

| File | Purpose |
|---|---|
| `server.py` | Run on server PC — type messages to broadcast |
| `client.py` | Run on each client PC — listens for messages |
| `simulate_100_clients.py` | Test with 100 fake clients on one machine |

---

## Quick Start

**1. Start server:**
```bash
python server.py
```

**2. Edit `client.py` — set server IP:**
```python
SERVER_HOST = "192.168.1.10"  # your server PC's LAN IP
```

**3. Run client on each PC:**
```bash
python client.py
```

**4. Type message in server → all clients receive it instantly.**

---

## Second PC Not Connecting?

- Find server IP: run `ipconfig` (Windows) or `ip a` (Linux)
- Update `SERVER_HOST` in `client.py`
- Allow firewall (run as Admin on server PC):
```cmd
netsh advfirewall firewall add rule name="Broadcast" dir=in action=allow protocol=TCP localport=9999
```
- Both PCs must be on the **same WiFi/router**

---

## Requirements
- Python 3.6+
- No external libraries needed
