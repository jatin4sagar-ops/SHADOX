# =============================================================
# SHADOX — main.py
# Entry point for the application.
# Run this file to launch SHADOX:  python main.py
# =============================================================

import tkinter as tk

# Import the login screen — this is the first screen users see
from gui.login_screen import show_login_screen


# ── Step 1: Create the root window ────────────────────────────
# tk.Tk() creates the single main window that the whole app runs in.
# Every screen (login, register, chat) reuses this same window.
root = tk.Tk()

# ── Step 2: Set the window title ──────────────────────────────
root.title("SHADOX")

# ── Step 3: Show the login screen ─────────────────────────────
# This builds the login widgets inside the root window.
# From here, all navigation (register → chat → logout) is handled
# by each screen replacing the widgets inside this same root window.
show_login_screen(root)

# ── Step 4: Start the Tkinter main loop ───────────────────────
# mainloop() keeps the window open and listens for user actions
# (button clicks, key presses, etc.) until the window is closed.
root.mainloop()