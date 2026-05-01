# =============================================================
# SHADOX — gui/chat_screen.py
# Main chat screen. Handles:
#   - Displaying and sending messages
#   - Live points updates
#   - Auto-refresh via root.after()
#   - Navigation to Profile, Leaderboard, Analytics, Logout
# =============================================================

import tkinter as tk
from tkinter import messagebox

from core.chat   import send_message, get_recent_messages
from core.points import add_points, get_points
from config      import CHAT_REFRESH_MS


def show_chat_screen(root, user):
    """
    Builds and displays the chat screen inside the root window.

    Args:
        root (tk.Tk): The main Tkinter window from main.py.
        user (dict) : {
                          "college_id" : str,
                          "codename"   : str,
                          "points"     : int
                      }
    """

    # ── Step 1: Configure window ───────────────────────────────
    root.title(f"SHADOX — {user['codename']}")
    root.geometry("680x520")
    root.resizable(False, False)
    root.configure(bg="#F5F5F5")

    # Clear all widgets from the previous screen
    for widget in root.winfo_children():
        widget.destroy()

    # ── Step 2: Auto-refresh job tracker ──────────────────────
    # Stored in a mutable list so all inner functions share it.
    refresh_job = [None]

    # ── Step 3: Cancel helper ──────────────────────────────────
    def cancel_refresh():
        """Safely cancels the auto-refresh loop before navigating away."""
        if refresh_job[0] is not None:
            root.after_cancel(refresh_job[0])
            refresh_job[0] = None

    # ── Step 4: Top frame — user info + nav buttons ────────────
    top_frame = tk.Frame(root, bg="#212121")
    top_frame.pack(fill="x")

    # Left side — codename and live points
    info_frame = tk.Frame(top_frame, bg="#212121")
    info_frame.pack(side="left", padx=14, pady=8)

    tk.Label(
        info_frame,
        text=f"You are:  {user['codename']}",
        font=("Helvetica", 11, "bold"),
        fg="white",
        bg="#212121"
    ).pack(anchor="w")

    points_label = tk.Label(
        info_frame,
        text=f"Points:  {user['points']}",
        font=("Helvetica", 10),
        fg="#B0BEC5",
        bg="#212121"
    )
    points_label.pack(anchor="w")

    # Right side — navigation buttons
    nav_frame = tk.Frame(top_frame, bg="#212121")
    nav_frame.pack(side="right", padx=14, pady=8)

    def nav_btn(parent, label, command):
        """Helper to create a consistent nav button."""
        return tk.Button(
            parent,
            text=label,
            font=("Helvetica", 9),
            fg="white",
            bg="#424242",
            activeforeground="white",
            activebackground="#616161",
            relief="flat",
            padx=8,
            pady=4,
            cursor="hand2",
            command=command
        )

    def go_profile():
        cancel_refresh()
        from gui.profile_screen import show_profile_screen
        show_profile_screen(root, user)

    def go_leaderboard():
        cancel_refresh()
        from gui.leaderboard_screen import show_leaderboard_screen
        show_leaderboard_screen(root, user)

    def go_analytics():
        try:
            from core.analytics import generate_user_activity_chart
            generate_user_activity_chart()
        except ImportError:
            messagebox.showinfo(
                "Analytics",
                "Analytics module not found.\nCreate core/analytics.py to enable this feature."
            )
        except Exception as e:
            messagebox.showerror("Analytics Error", str(e))

    def go_logout():
        cancel_refresh()
        root.configure(bg="white")
        from gui.login_screen import show_login_screen
        show_login_screen(root)

    nav_btn(nav_frame, "Profile",     go_profile).pack(side="left", padx=3)
    nav_btn(nav_frame, "Leaderboard", go_leaderboard).pack(side="left", padx=3)
    nav_btn(nav_frame, "Analytics",   go_analytics).pack(side="left", padx=3)
    nav_btn(nav_frame, "Logout",      go_logout).pack(side="left", padx=3)

    # ── Step 5: Middle frame — chat display ────────────────────
    chat_frame = tk.Frame(root, bg="#F5F5F5")
    chat_frame.pack(fill="both", expand=True, padx=12, pady=(10, 6))

    chat_display = tk.Text(
        chat_frame,
        state="disabled",       # Read-only — users cannot type here
        wrap="word",
        font=("Courier", 10),   # Monospace makes [HH:MM] timestamps align
        bg="white",
        fg="#212121",
        relief="solid",
        borderwidth=1,
        padx=8,
        pady=6
    )
    chat_display.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(chat_frame, command=chat_display.yview)
    scrollbar.pack(side="right", fill="y")
    chat_display.config(yscrollcommand=scrollbar.set)

    # ── Step 6: Bottom frame — message input ───────────────────
    input_frame = tk.Frame(root, bg="#F5F5F5")
    input_frame.pack(fill="x", padx=12, pady=(0, 12))

    message_entry = tk.Entry(
        input_frame,
        font=("Helvetica", 11),
        relief="solid",
        borderwidth=1
    )
    message_entry.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=4)
    message_entry.focus()

    send_btn = tk.Button(
        input_frame,
        text="Send",
        width=10,
        font=("Helvetica", 11),
        fg="white",
        bg="#2979FF",
        activeforeground="white",
        activebackground="#1565C0",
        relief="flat",
        cursor="hand2",
        command=lambda: handle_send()
    )
    send_btn.pack(side="right", ipady=4)

    # ── Step 7: refresh_chat() ────────────────────────────────

    def refresh_chat():
        """
        Fetches the latest messages from MongoDB and rewrites
        the chat display. Messages are formatted as:
        [HH:MM] Codename: Message text
        """
        messages = get_recent_messages()

        # Unlock, clear, rewrite, lock
        chat_display.config(state="normal")
        chat_display.delete("1.0", tk.END)

        for msg in messages:
            # Format the timestamp as HH:MM if it exists
            ts = msg.get("timestamp")
            if ts:
                time_str = ts.strftime("%H:%M")
            else:
                time_str = "--:--"

            line = f"[{time_str}] {msg['codename']}: {msg['text']}\n"
            chat_display.insert(tk.END, line)

        chat_display.config(state="disabled")
        chat_display.yview(tk.END)   # Scroll to newest message

    # ── Step 8: schedule_refresh() ────────────────────────────

    def schedule_refresh():
        """
        Calls refresh_chat() then schedules itself to run again
        after CHAT_REFRESH_MS milliseconds. Stores the job ID
        in refresh_job so it can be cancelled before navigating away.
        """
        refresh_chat()
        refresh_job[0] = root.after(CHAT_REFRESH_MS, schedule_refresh)

    # ── Step 9: handle_send() ─────────────────────────────────

    def handle_send():
        """
        Reads the input box, sends the message to MongoDB,
        awards points, updates the points label, clears the
        input box, and immediately refreshes the chat display.
        """
        text = message_entry.get()

        result = send_message(user["codename"], text)

        if result["success"]:
            # Award points for the message
            add_points(user["codename"])

            # Fetch the updated points total and refresh the label
            pts_result = get_points(user["codename"])
            if pts_result["success"]:
                user["points"] = pts_result["points"]   # Keep user dict in sync
                points_label.config(text=f"Points:  {pts_result['points']}")

            # Clear input and show the new message immediately
            message_entry.delete(0, tk.END)
            refresh_chat()

        else:
            messagebox.showerror("Send Failed", result["message"])

    # Pressing Enter sends the message
    root.bind("<Return>", lambda event: handle_send())

    # ── Step 10: Start the auto-refresh loop ──────────────────
    # schedule_refresh() calls refresh_chat() immediately,
    # then keeps polling every CHAT_REFRESH_MS milliseconds.
    schedule_refresh()