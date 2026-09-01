# Task 5: Chat Application

\# ⚡ Stark Tactical Multi-Room Chat Application



An asynchronous, multithreaded client-server communication suite built with Python, featuring raw TCP socket networking, structured JSON telemetry packets, local SQLite persistence, and a custom Tkinter holographic HUD interface.



\---



\## 🚀 Key Features



\- \*\*Multithreaded Server Relay:\*\* Handles concurrent client connections and room isolation (`#general`, `#tech`, `#ops`, `#weapons`) via Python's native `socket` and `threading` libraries.

\- \*\*Custom JSON Packet Protocol:\*\* Standardized action envelopes (`JOIN`, `MESSAGE`, `NOTIFICATION`, `HISTORY`) ensure robust serialization across network boundaries.

\- \*\*Holographic Mark-VII HUD (Tkinter GUI):\*\*

&#x20; - Animated Arc Reactor telemetry canvas.

&#x20; - Live frequency/channel switcher with dynamic buffer loading.

&#x20; - Native audio telemetry (`winsound`) alerts on incoming packets.

&#x20; - Built-in shortcuts (`:arc:`, `:fire:`, `:stark:`, `:robot:`) and terminal commands (`/clear`, `/ping`, `/roll`).

\- \*\*Persistent Data Store:\*\* Automatic session archiving via `sqlite3` to fetch recent channel logs on connection.



\---



\## 🛠️ Tech Stack \& Architecture



\- \*\*Language:\*\* Python 3.x

\- \*\*Networking:\*\* `socket` (TCP / IP), `threading`

\- \*\*Data Protocol:\*\* `json`

\- \*\*Database:\*\* `sqlite3`

\- \*\*GUI Engine:\*\* `tkinter`, `ttk`, `scrolledtext`

\- \*\*Audio Telemetry:\*\* `winsound`



\---



\## 📂 Project Structure	

ython-Task5-ChatApplication/

├── server.py               # Core multithreaded socket relay server \& SQLite logger

├── client.py               # Tactical Tkinter holographic client interface

├── generate\_title\_card.py  # Automation script for verification title cards

├── Task5\_TitleCard.png     # Generated demo video title card

└── README.md               # Technical project documentation

