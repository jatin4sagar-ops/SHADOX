# =============================================================
# SHADOX — core/ranks.py
# Maps a user's points total to a rank title string.
# Ranks are computed on the fly — nothing is stored in MongoDB.
# =============================================================


# ── Rank thresholds ───────────────────────────────────────────
# Each entry: (min_points, rank_label)
# Listed highest first so the first match wins.

RANK_TIERS = [
    (200, "Legend"),
    (100, "Veteran"),
    (50,  "Explorer"),
    (0,   "Rookie"),
]


# ── Main function ─────────────────────────────────────────────

def get_user_rank(points):
    """
    Returns the rank title for a given points value.

    Args:
        points (int): The user's current points total.

    Returns:
        str: Rank label — one of "Rookie", "Explorer",
             "Veteran", or "Legend".

    Examples:
        get_user_rank(0)   → "Rookie"
        get_user_rank(49)  → "Rookie"
        get_user_rank(50)  → "Explorer"
        get_user_rank(99)  → "Explorer"
        get_user_rank(100) → "Veteran"
        get_user_rank(200) → "Legend"
    """

    # Guard: treat negative or non-integer values as 0
    try:
        points = int(points)
    except (TypeError, ValueError):
        points = 0

    # Walk down from highest tier — first match wins
    for min_pts, rank_label in RANK_TIERS:
        if points >= min_pts:
            return rank_label

    # Fallback — should never be reached given RANK_TIERS includes 0
    return "Rookie"


# ── Test block ────────────────────────────────────────────────
# Run with:  python -m core.ranks

if __name__ == "__main__":
    print("=" * 40)
    print("  SHADOX — Rank System Test")
    print("=" * 40)

    test_cases = [0, 10, 49, 50, 85, 99, 100, 150, 199, 200, 350]

    for pts in test_cases:
        rank = get_user_rank(pts)
        print(f"  {pts:>4} pts  →  {rank}")

    print("=" * 40)