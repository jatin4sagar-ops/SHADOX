# =============================================================
# SHADOX — gui/leaderboard_screen.py
# Displays the top users ranked by points.
# Each row shows medal, rank title, codename, and points.
# =============================================================

import tkinter as tk

from db.db       import users_col
from core.ranks  import get_user_rank


# ── Medal and rank color mappings ─────────────────────────────

MEDALS = {
    1: "👑",
    2: "🥈",
    3: "🥉"
}

RANK_COLORS = {
    "Rookie"   : "#888888",   # Gray
    "Explorer" : "#2979FF",   # Blue
    "Veteran"  : "#8E24AA",   # Purple
    "Legend"   : "#F9A825",   # Gold
}


# ── Helper — fetch leaderboard data ───────────────────────────

def get_leaderboard(limit=10):
    """
    Fetches the top users from MongoDB sorted by points descending.

    Args:
        limit (int): Maximum number of users to return.

    Returns:
        list[dict]: Each entry has "codename" and "points".
                    Returns [] on error.
    """
    try:
        cursor = (
            users_col
            .find({}, {"_id": 0, "codename": 1, "points": 1})
            .sort("points", -1)
            .limit(limit)
        )
        return list(cursor)
    except Exception as e:
        print(f"[SHADOX] Error fetching leaderboard: {e}")
        return []


# ── Main screen function ───────────────────────────────────────

def show_leaderboard_screen(root, user):
    """
    Builds and displays the leaderboard screen.

    Args:
        root (tk.Tk): The main Tkinter window from main.py.
        user (dict) : The currently logged-in user's data
                      (passed through to return to chat).
    """

    # ── Step 1: Configure the window ──────────────────────────
    root.title("SHADOX — Leaderboard")
    root.geometry("500x560")
    root.resizable(False, False)
    root.configure(bg="#F5F5F5")

    for widget in root.winfo_children():
        widget.destroy()

    # ── Step 2: Page heading ───────────────────────────────────
    tk.Label(
        root,
        text="Leaderboard",
        font=("Helvetica", 22, "bold"),
        bg="#F5F5F5", fg="#212121"
    ).pack(pady=(28, 2))

    tk.Label(
        root,
        text="Top anonymous users by points",
        font=("Helvetica", 10),
        bg="#F5F5F5", fg="#757575"
    ).pack(pady=(0, 18))

    # ── Step 3: Leaderboard card ───────────────────────────────
    card = tk.Frame(root, bg="white", relief="solid", borderwidth=1)
    card.pack(fill="both", expand=True, padx=28, pady=(0, 14))

    # Column headers
    header = tk.Frame(card, bg="white")
    header.pack(fill="x", padx=12, pady=(10, 4))

    tk.Label(
        header, text="Rank",
        font=("Helvetica", 10, "bold"),
        bg="white", fg="#616161",
        width=5, anchor="w"
    ).pack(side="left")

    tk.Label(
        header, text="User",
        font=("Helvetica", 10, "bold"),
        bg="white", fg="#616161",
        anchor="w"
    ).pack(side="left", fill="x", expand=True)

    tk.Label(
        header, text="Pts",
        font=("Helvetica", 10, "bold"),
        bg="white", fg="#616161",
        width=6, anchor="e"
    ).pack(side="right")

    tk.Frame(card, height=1, bg="#EEEEEE").pack(fill="x")

    # ── Step 4: Fetch entries and build rows ───────────────────
    entries = get_leaderboard(limit=10)

    if not entries:
        tk.Label(
            card,
            text="No users found yet.",
            font=("Helvetica", 11),
            bg="white", fg="#9E9E9E",
            pady=24
        ).pack()

    else:
        for position, entry in enumerate(entries, start=1):
            rank       = get_user_rank(entry["points"])
            rank_color = RANK_COLORS.get(rank, "#888888")
            medal      = MEDALS.get(position, f"  {position}.")
            is_me      = entry["codename"] == user["codename"]

            # Row background — slightly tinted for the logged-in user
            row_bg = "#FFF8E1" if is_me else "white"

            row = tk.Frame(card, bg=row_bg)
            row.pack(fill="x", padx=12, pady=5)

            # Medal / position number
            tk.Label(
                row,
                text=medal,
                font=("Helvetica", 13),
                bg=row_bg,
                width=4,
                anchor="w"
            ).pack(side="left")

            # Rank title — colored by rank tier
            tk.Label(
                row,
                text=rank,
                font=("Helvetica", 9, "bold"),
                fg=rank_color,
                bg=row_bg,
                width=9,
                anchor="w"
            ).pack(side="left")

            # Codename — bold + "(you)" if it's the logged-in user
            name_text = f"{entry['codename']} (you)" if is_me else entry["codename"]
            name_font = ("Helvetica", 11, "bold") if is_me else ("Helvetica", 11)

            tk.Label(
                row,
                text=name_text,
                font=name_font,
                fg="#212121",
                bg=row_bg,
                anchor="w"
            ).pack(side="left", fill="x", expand=True)

            # Points — right-aligned
            tk.Label(
                row,
                text=str(entry["points"]),
                font=("Helvetica", 11, "bold"),
                fg=rank_color,
                bg=row_bg,
                width=6,
                anchor="e"
            ).pack(side="right")

            # Thin divider beneath each row (skip after last)
            if position < len(entries):
                tk.Frame(card, height=1, bg="#EEEEEE").pack(fill="x")

    # ── Step 5: Back to Chat button ────────────────────────────
    def go_back():
        root.configure(bg="white")
        from gui.chat_screen import show_chat_screen
        show_chat_screen(root, user)

    tk.Button(
        root,
        text="Back to Chat",
        width=20,
        font=("Helvetica", 11),
        bg="#212121",
        fg="white",
        activebackground="#424242",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=go_back
    ).pack(pady=(0, 24))