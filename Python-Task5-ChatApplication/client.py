import socket
import threading
import json
import time
import math
import random
import winsound
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

HOST = '127.0.0.1'
PORT = 65432

EMOJI_MAP = {
    ":arc:": "⚡",
    ":fire:": "🔥",
    ":skull:": "💀",
    ":robot:": "🤖",
    ":check:": "✅",
    ":stark:": "🕶️",
    ":shield:": "🛡️",
    ":target:": "🎯"
}

class StarkHolographicClient:
    def __init__(self, root):
        self.root = root
        self.root.title("STARK INDUSTRIES // MARK-VII COMM LINK")
        self.root.geometry("820x640")
        self.root.configure(bg="#06090f")
        self.root.minsize(760, 560)

        self.sock = None
        self.running = False
        self.buffer = ""
        self.current_room = "general"
        self.pulse_phase = 0.0

        self._build_login()

    def _build_login(self):
        self.login_frame = tk.Frame(self.root, bg="#06090f")
        self.login_frame.pack(expand=True)

        # Arc Reactor Logo Canvas
        self.login_canvas = tk.Canvas(self.login_frame, width=120, height=120, bg="#06090f", highlightthickness=0)
        self.login_canvas.pack(pady=10)
        self._draw_static_reactor(self.login_canvas, 60, 60)

        tk.Label(self.login_frame, text="STARK INDUSTRIES", font=("Consolas", 20, "bold"), fg="#00e5ff", bg="#06090f").pack()
        tk.Label(self.login_frame, text="SECURE NEURAL COMM LINK // PROTOCOL 10.4", font=("Consolas", 9), fg="#ffd600", bg="#06090f").pack(pady=(0, 20))

        # Inputs
        tk.Label(self.login_frame, text="CALLSIGN / OPERATOR ID:", font=("Consolas", 10, "bold"), fg="#8892b0", bg="#06090f").pack(anchor="w", padx=30)
        self.user_entry = tk.Entry(self.login_frame, font=("Consolas", 12), width=28, bg="#0d1527", fg="#00ffa3", insertbackground="#00ffa3", relief="flat")
        self.user_entry.insert(0, "Tony_Stark")
        self.user_entry.pack(padx=30, pady=6)

        tk.Label(self.login_frame, text="INITIAL FREQUENCY:", font=("Consolas", 10, "bold"), fg="#8892b0", bg="#06090f").pack(anchor="w", padx=30)
        self.room_combo = ttk.Combobox(self.login_frame, values=["general", "tech", "ops", "weapons"], state="readonly", font=("Consolas", 11), width=26)
        self.room_combo.current(0)
        self.room_combo.pack(padx=30, pady=6)

        btn = tk.Button(self.login_frame, text="INITIALIZE LINK", command=self.connect, font=("Consolas", 11, "bold"), bg="#00e5ff", fg="#06090f", activebackground="#00ffa3", relief="flat", padx=15, pady=6, cursor="hand2")
        btn.pack(pady=25)

    def _build_hud(self):
        self.login_frame.pack_forget()

        self.hud = tk.Frame(self.root, bg="#06090f")
        self.hud.pack(fill=tk.BOTH, expand=True, padx=14, pady=12)

        # Top Holographic Header Bar
        header = tk.Frame(self.hud, bg="#0d1527", padx=10, pady=6, highlightbackground="#00e5ff", highlightthickness=1)
        header.pack(fill=tk.X, pady=(0, 10))

        # Left Reactor animation canvas
        self.hud_canvas = tk.Canvas(header, width=44, height=44, bg="#0d1527", highlightthickness=0)
        self.hud_canvas.pack(side=tk.LEFT, padx=(0, 10))

        # Header Info
        info_frame = tk.Frame(header, bg="#0d1527")
        info_frame.pack(side=tk.LEFT)
        self.node_lbl = tk.Label(info_frame, text=f"OPERATOR: {self.username.upper()}", font=("Consolas", 11, "bold"), fg="#00e5ff", bg="#0d1527")
        self.node_lbl.pack(anchor="w")
        self.telemetry_lbl = tk.Label(info_frame, text="SYS: OPTIMAL | LINK: ENCRYPTED | PING: 1ms", font=("Consolas", 8), fg="#ffd600", bg="#0d1527")
        self.telemetry_lbl.pack(anchor="w")

        # Channel Selector Buttons
        channel_bar = tk.Frame(header, bg="#0d1527")
        channel_bar.pack(side=tk.RIGHT, pady=4)
        for room in ["general", "tech", "ops", "weapons"]:
            b = tk.Button(channel_bar, text=f"#{room.upper()}", command=lambda r=room: self.switch_room(r), font=("Consolas", 9, "bold"), bg="#06090f", fg="#00ffa3", activebackground="#00e5ff", activeforeground="#06090f", relief="flat", padx=6, pady=2, cursor="hand2")
            b.pack(side=tk.LEFT, padx=3)

        # Main Feed and Sidebar split
        main_split = tk.Frame(self.hud, bg="#06090f")
        main_split.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Console Log Feed
        self.feed = scrolledtext.ScrolledText(main_split, wrap=tk.WORD, font=("Consolas", 10), bg="#04060a", fg="#ccd6f6", insertbackground="#00e5ff", relief="flat", highlightbackground="#1f2d4d", highlightthickness=1)
        self.feed.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.feed.config(state=tk.DISABLED)

        # Tactical Telemetry Sidebar
        sidebar = tk.Frame(main_split, width=180, bg="#0d1527", highlightbackground="#1f2d4d", highlightthickness=1, padx=8, pady=8)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="TELEMETRY", font=("Consolas", 10, "bold"), fg="#00e5ff", bg="#0d1527").pack(anchor="w")
        tk.Label(sidebar, text="-----------------", font=("Consolas", 8), fg="#1f2d4d", bg="#0d1527").pack(anchor="w")

        self.side_status = tk.Label(sidebar, text=f"CHANNEL:\n#{self.current_room}\n\nCORE: 4.8 GHz\nBUFFER: OK\nPACKETS: 0", justify=tk.LEFT, font=("Consolas", 9), fg="#8892b0", bg="#0d1527")
        self.side_status.pack(anchor="w", pady=6)

        tk.Label(sidebar, text="SHORTCUTS", font=("Consolas", 10, "bold"), fg="#ffd600", bg="#0d1527").pack(anchor="w", pady=(15, 0))
        tk.Label(sidebar, text="-----------------", font=("Consolas", 8), fg="#1f2d4d", bg="#0d1527").pack(anchor="w")
        tk.Label(sidebar, text="/clear -> Purge\n/ping  -> Latency\n/roll  -> Random\n:arc:  -> ⚡\n:fire: -> 🔥\n:stark:-> 🕶️", justify=tk.LEFT, font=("Consolas", 8), fg="#00ffa3", bg="#0d1527").pack(anchor="w", pady=4)

        # Input Dock
        dock = tk.Frame(self.hud, bg="#06090f")
        dock.pack(fill=tk.X)

        self.entry = tk.Entry(dock, font=("Consolas", 11), bg="#0d1527", fg="#00ffa3", insertbackground="#00ffa3", relief="flat", highlightbackground="#00e5ff", highlightthickness=1)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=6)
        self.entry.bind("<Return>", lambda e: self.send_packet())

        send_btn = tk.Button(dock, text="TRANSMIT", command=self.send_packet, font=("Consolas", 10, "bold"), bg="#00e5ff", fg="#06090f", activebackground="#00ffa3", relief="flat", padx=14, pady=4, cursor="hand2")
        send_btn.pack(side=tk.RIGHT)

        self._start_reactor_animation()

    def _draw_static_reactor(self, canvas, cx, cy):
        canvas.create_oval(cx-40, cy-40, cx+40, cy+40, outline="#00e5ff", width=2)
        canvas.create_oval(cx-26, cy-26, cx+26, cy+26, outline="#ffd600", width=2)
        canvas.create_oval(cx-12, cy-12, cx+12, cy+12, fill="#00e5ff", outline="")

    def _start_reactor_animation(self):
        if not self.running:
            return
        self.hud_canvas.delete("all")
        cx, cy = 22, 22
        self.pulse_phase += 0.25
        glow = math.sin(self.pulse_phase) * 3 + 12

        # Outer pulsing rings
        self.hud_canvas.create_oval(cx-glow, cy-glow, cx+glow, cy+glow, outline="#00e5ff", width=1)
        self.hud_canvas.create_oval(cx-7, cy-7, cx+7, cy+7, outline="#ffd600", width=1)
        self.hud_canvas.create_oval(cx-3, cy-3, cx+3, cy+3, fill="#00ffa3", outline="")

        self.root.after(80, self._start_reactor_animation)

    def connect(self):
        self.username = self.user_entry.get().strip() or "Tony_Stark"
        self.current_room = self.room_combo.get()

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            self.running = True

            join_packet = {"action": "JOIN", "username": self.username, "room": self.current_room}
            self.sock.sendall((json.dumps(join_packet) + "\n").encode('utf-8'))

            self._build_hud()
            threading.Thread(target=self.receive_loop, daemon=True).start()
            winsound.Beep(1200, 80)
        except Exception as e:
            messagebox.showerror("HUD Error", f"Core comm link failed:\n{e}")

    def switch_room(self, new_room):
        if new_room == self.current_room or not self.running:
            return
        self.current_room = new_room
        self.side_status.config(text=f"CHANNEL:\n#{self.current_room}\n\nCORE: 4.8 GHz\nBUFFER: OK\nPACKETS: ACTIVE")
        self._append(f"\n[SYSTEM] Shifting frequency to sector #{new_room.upper()}...\n")
        join_packet = {"action": "JOIN", "username": self.username, "room": self.current_room}
        self.sock.sendall((json.dumps(join_packet) + "\n").encode('utf-8'))

    def receive_loop(self):
        packet_count = 0
        while self.running:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                if not data:
                    break
                self.buffer += data
                while "\n" in self.buffer:
                    line, self.buffer = self.buffer.split("\n", 1)
                    if not line.strip():
                        continue
                    packet = json.loads(line)
                    ptype = packet.get("type")
                    packet_count += 1

                    if ptype == "MESSAGE":
                        sender = packet.get("username")
                        msg = packet.get("message")
                        ts = packet.get("timestamp")
                        tag = " [YOU]" if sender == self.username else ""
                        self._append(f"[{ts}] {sender}{tag}: {msg}\n")
                        if sender != self.username:
                            winsound.Beep(950, 60)

                    elif ptype == "NOTIFICATION":
                        self._append(f"[{packet.get('timestamp')}] ⚡ {packet.get('message')} ⚡\n")

                    elif ptype == "HISTORY":
                        self._append("=== ARCHIVED TELEMETRY FEED ===\n")
                        for h in packet.get("history", []):
                            self._append(f"[{h['timestamp']}] {h['username']}: {h['message']}\n")
                        self._append("================================\n")
            except Exception:
                break
        self._append("\n[!] CRITICAL: Core relay link terminated.\n")

    def _append(self, text):
        self.feed.config(state=tk.NORMAL)
        self.feed.insert(tk.END, text)
        self.feed.see(tk.END)
        self.feed.config(state=tk.DISABLED)

    def send_packet(self):
        raw_msg = self.entry.get().strip()
        if not raw_msg or not self.running:
            return

        self.entry.delete(0, tk.END)

        # Tactical Local Commands
        if raw_msg == "/clear":
            self.feed.config(state=tk.NORMAL)
            self.feed.delete('1.0', tk.END)
            self.feed.config(state=tk.DISABLED)
            return
        elif raw_msg == "/ping":
            self._append(f"[SYS] Ping to host {HOST}: <1ms (Local Relay Loopback)\n")
            return
        elif raw_msg == "/roll":
            raw_msg = f"rolled a tactical value of {random.randint(1, 100)} 🎯"

        # Auto parse emoji triggers
        for code, emoji in EMOJI_MAP.items():
            raw_msg = raw_msg.replace(code, emoji)

        packet = {"action": "MESSAGE", "message": raw_msg}
        try:
            self.sock.sendall((json.dumps(packet) + "\n").encode('utf-8'))
        except Exception:
            self._append("[!] ERROR: Packet lost in transmission.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = StarkHolographicClient(root)
    root.mainloop()