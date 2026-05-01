# =============================================================
# SHADOX — core/badges.py
# Awards achievement badges to users based on their activity.
# Badges are computed on the fly from MongoDB data — they are
# not stored in the database, just calculated when needed.
# =============================================================

# Import both collections from the database layer
from db.db import messages_col, users_col


# ── Badge definitions ─────────────────────────────────────────
# Each entry is (threshold, badge_label).
# The check compares the user's count/points against the threshold.

MESSAGE_BADGES = [
    (1,  "First Message"),
    (10, "Chatter"),
    (50, "Power User"),
]

POINTS_BADGES = [
    (50,  "Bronze Member"),
    (100, "Silver Member"),
    (200, "Gold Member"),
]


# ── Main function ─────────────────────────────────────────────

def get_user_badges(codename):
    """
    Calculates and returns all badges earned by a user.

    Steps:
        1. Validate the codename.
        2. Count how many messages the user has sent.
        3. Fetch the user's current points from MongoDB.
        4. Compare both values against the badge thresholds.
        5. Return the list of earned badge strings.

    Args:
        codename (str): The user's anonymous codename.

    Returns:
        list[str]: Badges the user has earned, e.g.
                   ["First Message", "Chatter", "Bronze Member"]
                   Returns an empty list if no badges are earned
                   or if an error occurs.
    """

    # ── Step 1: Validate input ────────────────────────────────
    if not codename or not codename.strip():
        print("[SHADOX] get_user_badges: codename is empty.")
        return []

    earned_badges = []

    # ── Step 2: Count messages sent by this user ──────────────
    try:
        message_count = messages_col.count_documents({"codename": codename})
    except Exception as e:
        print(f"[SHADOX] Error counting messages: {e}")
        message_count = 0

    # ── Step 3: Fetch the user's points ───────────────────────
    try:
        user = users_col.find_one(
            {"codename": codename},
            {"_id": 0, "points": 1}   # Only fetch the points field
        )
        points = user["points"] if user else 0
    except Exception as e:
        print(f"[SHADOX] Error fetching points: {e}")
        points = 0

    # ── Step 4: Check message-based badges ────────────────────
    # Award every badge whose threshold the user has reached or passed.
    for threshold, badge in MESSAGE_BADGES:
        if message_count >= threshold:
            earned_badges.append(badge)

    # ── Step 5: Check points-based badges ─────────────────────
    for threshold, badge in POINTS_BADGES:
        if points >= threshold:
            earned_badges.append(badge)

    return earned_badges


# ── Test block ────────────────────────────────────────────────
# Run with:  python -m core.badges
# This lets you quickly verify badge logic without opening the GUI.

if __name__ == "__main__":
    print("=" * 44)
    print("  SHADOX — Badge System Test")
    print("=" * 44)

    # Ask for a codename to test with
    test_codename = input("Enter a codename to check badges for: ").strip()

    if not test_codename:
        print("No codename entered. Exiting.")
    else:
        badges = get_user_badges(test_codename)

        print(f"\nCodename : {test_codename}")

        # Also print raw stats for easier debugging
        try:
            msg_count = messages_col.count_documents({"codename": test_codename})
            user_doc  = users_col.find_one({"codename": test_codename}, {"_id": 0, "points": 1})
            points    = user_doc["points"] if user_doc else 0
            print(f"Messages : {msg_count}")
            print(f"Points   : {points}")
        except Exception as e:
            print(f"Could not fetch stats: {e}")

        print()
        if badges:
            print(f"Badges earned ({len(badges)}):")
            for badge in badges:
                print(f"  ★  {badge}")
        else:
            print("No badges earned yet. Keep chatting!")

    print("=" * 44)