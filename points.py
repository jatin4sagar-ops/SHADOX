# =============================================================
# SHADOX — core/points.py
# Handles the points system for users.
# Points are stored inside each user's document in MongoDB.
# =============================================================

# Import the users collection from the database layer
from db.db import users_col

# Import points-related constants from config
from config import POINTS_PER_MESSAGE


# ── Add points ────────────────────────────────────────────────

def add_points(codename):
    """
    Awards POINTS_PER_MESSAGE points to a user after they send a message.

    Steps:
        1. Validate the codename is not empty.
        2. Check that the user actually exists in MongoDB.
        3. Use MongoDB's $inc operator to add points atomically.
        4. Return a success or error result.

    Args:
        codename (str): The user's anonymous codename, e.g. "SilentFalcon".

    Returns:
        dict: {
            "success": bool,
            "message": str   ← human-readable result description
        }
    """

    # ── Step 1: Validate input ────────────────────────────────
    if not codename or not codename.strip():
        return {"success": False, "message": "Codename is missing."}

    # ── Step 2: Check the user exists ────────────────────────
    user = users_col.find_one({"codename": codename})

    if not user:
        return {"success": False, "message": f"User '{codename}' not found."}

    # ── Step 3: Add points using MongoDB's $inc operator ──────
    # $inc increments the field by the given amount in one safe
    # operation — no need to read the old value, add, then write.
    try:
        users_col.update_one(
            {"codename": codename},           # Find this user
            {"$inc": {"points": POINTS_PER_MESSAGE}}  # Add points
        )
        return {
            "success": True,
            "message": f"+{POINTS_PER_MESSAGE} points awarded to {codename}."
        }

    except Exception as e:
        return {"success": False, "message": f"Failed to update points: {str(e)}"}


# ── Get points ────────────────────────────────────────────────

def get_points(codename):
    """
    Retrieves the current points total for a user.

    Steps:
        1. Validate the codename is not empty.
        2. Look up the user document in MongoDB.
        3. Return their current points value, or an error if not found.

    Args:
        codename (str): The user's anonymous codename.

    Returns:
        dict: On success —
                {
                    "success": True,
                    "points" : int   ← current points total
                }
              On failure —
                {
                    "success": False,
                    "message": str
                }
    """

    # ── Step 1: Validate input ────────────────────────────────
    if not codename or not codename.strip():
        return {"success": False, "message": "Codename is missing."}

    # ── Step 2: Fetch only the points field from MongoDB ──────
    # We pass a projection so MongoDB returns just the one field
    # we need instead of the entire user document.
    try:
        user = users_col.find_one(
            {"codename": codename},      # Find this user
            {"_id": 0, "points": 1}      # Return only the points field
        )

        # ── Step 3: Return points or error ────────────────────
        if not user:
            return {"success": False, "message": f"User '{codename}' not found."}

        return {
            "success": True,
            "points" : user["points"]
        }

    except Exception as e:
        return {"success": False, "message": f"Failed to fetch points: {str(e)}"}
    
def get_user_level(points):
    """
    Returns level name based on total points.
    """

    if points <= 20:
        return "Shadow Novice"

    elif points <= 50:
        return "Shadow Apprentice"

    elif points <= 100:
        return "Shadow"

    elif points <= 200:
        return "Shadow Master"

    else:
        return "KING"
    
def get_leaderboard(top_n=5):
    """
    Returns top users sorted by points.
    """

    from db.db import users_col

    try:
        users = list(
            users_col
            .find({}, {"_id": 0, "codename": 1, "points": 1})
            .sort("points", -1)
            .limit(top_n)
        )

        return users

    except Exception as e:
        print(f"[SHADOX] Leaderboard error: {e}")
        return []