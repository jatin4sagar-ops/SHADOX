# =============================================================
# SHADOX — gui/profile_screen.py
# Displays the logged-in user's full profile with:
# codename, college ID, points, rank, level progress bar,
# streaks, and achievement badges.
# =============================================================

import tkinter as tk

from core.badges  import get_user_badges
from core.streaks import get_streak
from core.ranks   import get_user_rank


# ── Level configuration ───────────────────────────────────────
# Each entry: (min_points, max_points, label, hex_color)
# Level 4 has no ceiling — progress bar shows 100%.

LEVELS = [
    (0,   50,  "Level 1 — Newcomer", "#888888"),   # Gray
    (50,  100, "Level 2 — Regular",  "#2979FF"),   # Blue
    (100, 200, "Level 3 — Expert",   "#8E24AA"),   # Purple
    (200, 200, "Level 4 — Legend",   "#F9A825"),   # Gold
]

# Badge name → emoji prefix mapping
BADGE_ICONS = {
    "First Message" : "🔥",
    "Chatter"       : "💬",
    "Power User"    : "⚡",
    "Bronze Member" : "🏅",
    "Silver Member" : "🥈",
    "Gold Member"   : "🥇",
}

# Rank → color mapping (mirrors level colors for consistency)
RANK_COLORS = {
    "Rookie"   : "#888888",   # Gray
    "Explorer" : "#2979FF",   # Blue
    "Veteran"  : "#8E24AA",   # Purple
    "Legend"   : "#F9A825",   # Gold
}


# ── Level helpers ─────────────────────────────────────────────

def get_level(points):
    """Returns the level label string for a given points value."""
    if points >= 200:
        return "Level 4 — Legend"
    elif points >= 100:
        return "Level 3 — Expert"
    elif points >= 50:
        return "Level 2 — Regular"
    else:
        return "Level 1 — Newcomer"


def get_level_meta(points):
    """
    Returns label, hex color, progress fraction, and pts display
    string for the current level.
    """
    for min_pts, max_pts, label, color in LEVELS:
        if points < max_pts or (max_pts == min_pts and points >= 200):
            if max_pts == min_pts:
                return {
                    "label": label, "color": color,
                    "fraction": 1.0, "pts_text": f"{points} pts — MAX"
                }
            progress = (points - min_pts) / (max_pts - min_pts)
            return {
                "label": label, "color": color,
                "fraction": min(progress, 1.0),
                "pts_text": f"{points} / {max_pts} pts"
            }
    return {"label": get_level(points), "color": "#888888",
            "fraction": 1.0, "pts_text": f"{points} pts"}


# ── Progress bar widget ───────────────────────────────────────

def draw_progress_bar(parent, fraction, color, width=340, height=18):
    """Draws a filled Canvas progress bar."""
    canvas = tk.Canvas(
        parent, width=width, height=height,
        bg="#E0E0E0", highlightthickness=1,
        highlightbackground="#BDBDBD", relief="flat"
    )
    canvas.pack(pady=(2, 0))
    fill_width = max(6, int(width * fraction))
    canvas.create_rectangle(0, 0, fill_width, height, fill=color, outline="")


# ── Card row helper ───────────────────────────────────────────

def add_card_row(parent, label_text, value_text,
                 bold_value=False, value_color=None):
    """
    Adds a two-column label row inside a card frame with a
    thin gray divider beneath it.
    """
    row = tk.Frame(parent, bg="white")
    row.pack(fill="x", padx=16, pady=9)

    tk.Label(
        row, text=label_text,
        font=("Helvetica", 10), fg="#616161",
        bg="white", anchor="w", width=16
    ).pack(side="left")

    value_font = ("Helvetica", 11, "bold") if bold_value else ("Helvetica", 11)
    tk.Label(
        row, text=value_text,
        font=value_font,
        fg=value_color if value_color else "#212121",
        bg="white", anchor="w"
    ).pack(side="left")

    tk.Frame(parent, height=1, bg="#EEEEEE").pack(fill="x")


# ── Main screen function ───────────────────────────────────────

def show_profile_screen(root, user):
    """
    Builds and displays the profile screen.

    Args:
        root (tk.Tk): The main Tkinter window from main.py.
        user (dict) : {
                          "college_id" : str,
                          "codename"   : str,
                          "points"     : int
                      }
    """

    # ── Step 1: Configure window ───────────────────────────────
    root.title("SHADOX — Profile")
    root.geometry("480x720")
    root.resizable(False, False)
    root.configure(bg="#F5F5F5")

    for widget in root.winfo_children():
        widget.destroy()

    # ── Step 2: Fetch all data before building UI ──────────────
    points     = user["points"]
    rank       = get_user_rank(points)
    rank_color = RANK_COLORS.get(rank, "#888888")
    level_meta = get_level_meta(points)

    streak_result  = get_streak(user["codename"])
    current_streak = streak_result.get("current_streak", 0) if streak_result["success"] else 0
    best_streak    = streak_result.get("best_streak",    0) if streak_result["success"] else 0

    badges = get_user_badges(user["codename"])

    # ── Step 3: Page heading ───────────────────────────────────
    tk.Label(
        root, text="My Profile",
        font=("Helvetica", 22, "bold"),
        bg="#F5F5F5", fg="#212121"
    ).pack(pady=(24, 2))

    tk.Label(
        root, text="Your anonymous identity and stats",
        font=("Helvetica", 10),
        bg="#F5F5F5", fg="#757575"
    ).pack(pady=(0, 14))

    # ── Step 4: Profile card ───────────────────────────────────
    card = tk.Frame(root, bg="white", relief="solid", borderwidth=1)
    card.pack(fill="x", padx=28, pady=(0, 12))

    tk.Frame(card, height=1, bg="#EEEEEE").pack(fill="x")   # Top border

    add_card_row(card, "Codename",   user["codename"],  bold_value=True)
    add_card_row(card, "College ID", user["college_id"])
    add_card_row(card, "Points",     str(points),       bold_value=True)

    # ── Rank row — placed between Points and Level ─────────────
    add_card_row(
        card,
        "Rank",
        rank,
        bold_value=True,
        value_color=rank_color
    )

    # ── Level row ──────────────────────────────────────────────
    add_card_row(
        card,
        "Level",
        level_meta["label"],
        bold_value=True,
        value_color=level_meta["color"]
    )

    # ── Level progress bar ─────────────────────────────────────
    bar_frame = tk.Frame(card, bg="white")
    bar_frame.pack(fill="x", padx=16, pady=(4, 10))

    draw_progress_bar(bar_frame, level_meta["fraction"], level_meta["color"])

    tk.Label(
        bar_frame,
        text=level_meta["pts_text"],
        font=("Helvetica", 9),
        fg="#757575", bg="white"
    ).pack(pady=(3, 0))

    tk.Frame(card, height=1, bg="#EEEEEE").pack(fill="x")

    # ── Streak rows ────────────────────────────────────────────
    add_card_row(card, "Current Streak", f"🔥  {current_streak}")
    add_card_row(card, "Best Streak",    f"🏆  {best_streak}")

    # ── Step 5: Badges section ─────────────────────────────────
    badges_frame = tk.Frame(root, bg="white", relief="solid", borderwidth=1)
    badges_frame.pack(fill="x", padx=28, pady=(0, 14))

    tk.Label(
        badges_frame,
        text="🏅  Badges Earned",
        font=("Helvetica", 11, "bold"),
        bg="white", fg="#212121", anchor="w"
    ).pack(fill="x", padx=16, pady=(10, 6))

    tk.Frame(badges_frame, height=1, bg="#EEEEEE").pack(fill="x")

    if badges:
        for badge in badges:
            icon = BADGE_ICONS.get(badge, "★")
            tk.Label(
                badges_frame,
                text=f"   {icon}  {badge}",
                font=("Helvetica", 11),
                bg="white", fg="#212121", anchor="w"
            ).pack(fill="x", padx=16, pady=4)
        tk.Frame(badges_frame, height=6, bg="white").pack()
    else:
        tk.Label(
            badges_frame,
            text="   No badges earned yet.",
            font=("Helvetica", 11),
            bg="white", fg="#9E9E9E", anchor="w"
        ).pack(fill="x", padx=16, pady=10)

    # ── Step 6: Back to Chat button ────────────────────────────
    def go_back():
        root.configure(bg="white")
        from gui.chat_screen import show_chat_screen
        show_chat_screen(root, user)

    tk.Button(
        root,
        text="Back to Chat",
        width=20,
        font=("Helvetica", 11),
        bg=rank_color,            # Button tinted to match user's rank color
        fg="white",
        activebackground=rank_color,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=go_back
    ).pack(pady=(0, 24))