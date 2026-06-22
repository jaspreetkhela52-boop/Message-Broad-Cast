"""
Broadcast Server
- Accepts up to 100 clients on the local network
- Type a message and press Enter to send it to ALL clients
- Each client is handled in its own thread
"""

import socket
import threading

HOST = "0.0.0.0"   # Listen on all network interfaces
PORT = 9999
MAX_CLIENTS = 100

clients = []          # List of connected client sockets
clients_lock = threading.Lock()   # Thread-safe access to the list


def handle_client(conn, addr):
    """Keeps the client connection alive and removes it when disconnected."""
    print(f"[+] Client connected: {addr}")
    with clients_lock:
        clients.append(conn)

    try:
        while True:
            # Block here — we only detect if the client disconnects
            data = conn.recv(1024)
            if not data:
                break   # Client closed the connection
    except (ConnectionResetError, OSError):
        pass   # Client dropped unexpectedly
    finally:
        with clients_lock:
            clients.remove(conn)
        conn.close()
        print(f"[-] Client disconnected: {addr}")


def broadcast(message: str):
    """Send a message to every connected client."""
    encoded = (message + "\n").encode("utf-8")
    dead = []

    with clients_lock:
        for conn in clients:
            try:
                conn.sendall(encoded)
            except OSError:
                dead.append(conn)   # Mark broken connections

        for conn in dead:
            clients.remove(conn)
            conn.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CLIENTS)

    print(f"[*] Server started on port {PORT}. Waiting for clients…")
    print("[*] Type a message and press Enter to broadcast.\n")

    # Accept clients in a background thread
    def accept_loop():
        while True:
            try:
                conn, addr = server_socket.accept()
                t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                t.start()
            except OSError:
                break

    accept_thread = threading.Thread(target=accept_loop, daemon=True)
    accept_thread.start()

    # Main thread: read user input and broadcast
    try:
        while True:
            message = input()
            if message.lower() == "quit":
                print("[*] Shutting down server.")
                break
            if clients:
                broadcast(message)
                print(f"[>] Broadcast to {len(clients)} client(s): {message}")
            else:
                print("[!] No clients connected yet.")
    except KeyboardInterrupt:
        print("\n[*] Server interrupted.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
