"""
Broadcast Client
- Connects to the server and listens for messages
- Prints every message received from the server
- Does NOT send anything back
"""

import socket
import sys

SERVER_HOST = "127.0.0.1"   # Change to the server's IP on your LAN, e.g. "192.168.1.10"
SERVER_PORT = 9999


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"[*] Connected to server at {SERVER_HOST}:{SERVER_PORT}")
        print("[*] Waiting for broadcast messages…\n")
    except ConnectionRefusedError:
        print(f"[!] Could not connect to {SERVER_HOST}:{SERVER_PORT}. Is the server running?")
        sys.exit(1)

    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                print("[!] Server closed the connection.")
                break
            print(f"[Server] {data.decode('utf-8').strip()}")
    except KeyboardInterrupt:
        print("\n[*] Client disconnected by user.")
    except (ConnectionResetError, OSError) as e:
        print(f"[!] Connection lost: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()
