import socket
import threading
import json
import sqlite3
from datetime import datetime

HOST = '127.0.0.1'
PORT = 65432

# Thread-safe SQLite helper
def get_db():
    conn = sqlite3.connect('chat_history.db', timeout=10)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room TEXT,
            username TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    return conn

# Active sockets: {client_socket: {'username': str, 'room': str}}
clients = {}
lock = threading.Lock()

def broadcast(payload, target_room, sender_socket=None):
    raw_data = (json.dumps(payload) + "\n").encode('utf-8')
    with lock:
        for sock, info in list(clients.items()):
            if info.get('room') == target_room and sock != sender_socket:
                try:
                    sock.sendall(raw_data)
                except Exception:
                    sock.close()
                    if sock in clients:
                        del clients[sock]

def handle_client(client_socket, address):
    print(f"[+] Node linked from {address}")
    buffer = ""
    db = get_db()
    cursor = db.cursor()
    try:
        while True:
            chunk = client_socket.recv(1024).decode('utf-8')
            if not chunk:
                break
            buffer += chunk
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if not line.strip():
                    continue
                packet = json.loads(line)
                action = packet.get("action")

                if action == "JOIN":
                    username = packet.get("username", "Anonymous")
                    room = packet.get("room", "general")
                    with lock:
                        clients[client_socket] = {"username": username, "room": room}

                    # Fetch previous conversation logs
                    cursor.execute("SELECT username, message, timestamp FROM messages WHERE room = ? ORDER BY id DESC LIMIT 15", (room,))
                    history = cursor.fetchall()[::-1]
                    hist_packet = {
                        "type": "HISTORY",
                        "history": [{"username": h[0], "message": h[1], "timestamp": h[2]} for h in history]
                    }
                    client_socket.sendall((json.dumps(hist_packet) + "\n").encode('utf-8'))

                    # Announce connection
                    broadcast({
                        "type": "NOTIFICATION",
                        "message": f"--> {username} connected to #{room}",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    }, room, sender_socket=client_socket)

                elif action == "MESSAGE":
                    with lock:
                        sender_info = clients.get(client_socket, {})
                        username = sender_info.get("username", "Anonymous")
                        room = sender_info.get("room", "general")

                    text = packet.get("message", "").strip()
                    ts = datetime.now().strftime("%H:%M:%S")

                    if text:
                        cursor.execute("INSERT INTO messages (room, username, message, timestamp) VALUES (?, ?, ?, ?)",
                                       (room, username, text, ts))
                        db.commit()

                        # Broadcast to everyone in the room (including sender)
                        broadcast({
                            "type": "MESSAGE",
                            "username": username,
                            "message": text,
                            "timestamp": ts
                        }, room)

    except Exception as e:
        print(f"[!] Error on {address}: {e}")
    finally:
        with lock:
            if client_socket in clients:
                info = clients[client_socket]
                room = info.get("room")
                user = info.get("username")
                del clients[client_socket]
                broadcast({
                    "type": "NOTIFICATION",
                    "message": f"<-- {user} disconnected.",
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }, room)
        client_socket.close()
        db.close()
        print(f"[-] Node offline: {address}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)
    print(f"[*] Comm Relay Server active on {HOST}:{PORT}...")
    while True:
        client_sock, addr = server.accept()
        t = threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True)
        t.start()

if __name__ == "__main__":
    start_server()