# =============================================================
# SHADOX — core/auth.py
# Handles user registration and login.
# All user data is stored in the MongoDB `users` collection.
# =============================================================

from datetime import datetime

from pymongo.errors import DuplicateKeyError

# Import the users collection from the database layer
from db.db import users_col

# Import the codename generator
from core.codename import generate_codename

# Import app-wide constants
from config import POINTS_PER_REGISTER


# ── Helper ────────────────────────────────────────────────────

def _codename_is_taken(codename):
    """
    Checks whether a codename is already assigned to another user.

    Args:
        codename (str): The codename to check.

    Returns:
        bool: True if taken, False if available.
    """
    return users_col.find_one({"codename": codename}) is not None


# ── Register ──────────────────────────────────────────────────

def register_user(college_id, password):
    """
    Creates a new SHADOX account for a student.

    Steps:
        1. Validate that inputs are not empty.
        2. Check MongoDB — reject if the College ID is already registered.
        3. Generate a unique anonymous codename.
        4. Build the user document and insert it into MongoDB.
        5. Return a success message, or an error message if anything fails.

    Args:
        college_id (str): The student's college ID (used as username).
        password   (str): Plain-text password chosen by the student.

    Returns:
        dict: {
            "success": bool,
            "message": str
        }
    """

    # ── Step 1: Basic input validation ────────────────────────
    if not college_id or not college_id.strip():
        return {"success": False, "message": "College ID cannot be empty."}

    if not password or not password.strip():
        return {"success": False, "message": "Password cannot be empty."}

    # Normalise: strip whitespace, keep original casing
    college_id = college_id.strip()

    # ── Step 2: Check if the College ID is already registered ─
    existing_user = users_col.find_one({"college_id": college_id})
    if existing_user:
        return {"success": False, "message": "This College ID is already registered."}

    # ── Step 3: Generate a unique anonymous codename ──────────
    # Keep generating until we find one that no other user has.
    codename = generate_codename()
    attempts = 0

    while _codename_is_taken(codename):
        codename = generate_codename()
        attempts += 1
        # Safety valve — stops an infinite loop if the word pool is exhausted
        if attempts > 100:
            return {
                "success": False,
                "message": "Could not generate a unique codename. Try again."
            }

    # ── Step 4: Build the user document ──────────────────────
    # NOTE: For a real production app you should hash the password
    # (e.g. with bcrypt). For this MVP it is stored as plain text
    # to keep the code beginner-friendly.
    user_document = {
        "college_id" : college_id,
        "password"   : password,           # Plain text — see note above
        "codename"   : codename,           # e.g. "SilentFalcon"
        "points"     : POINTS_PER_REGISTER, # Starting bonus from config.py
        "created_at" : datetime.now()
    }

    # ── Step 5: Insert into MongoDB ───────────────────────────
    try:
        users_col.insert_one(user_document)
        return {
            "success" : True,
            "message" : f"Registration successful! Your codename is: {codename}"
        }

    except DuplicateKeyError:
        # The unique index on college_id caught a race condition
        return {"success": False, "message": "This College ID is already registered."}

    except Exception as e:
        return {"success": False, "message": f"Registration failed: {str(e)}"}


# ── Login ─────────────────────────────────────────────────────

def login_user(college_id, password):
    """
    Verifies a student's credentials and returns their profile.

    Steps:
        1. Validate that inputs are not empty.
        2. Look up the College ID in MongoDB.
        3. Check that the password matches.
        4. Return the user document on success, or an error message.

    Args:
        college_id (str): The student's college ID.
        password   (str): The password entered at the login screen.

    Returns:
        dict: On success —
                {
                    "success" : True,
                    "message" : str,
                    "user"    : {
                        "college_id" : str,
                        "codename"   : str,
                        "points"     : int,
                        "created_at" : datetime
                    }
                }
              On failure —
                {
                    "success": False,
                    "message": str
                }
    """

    # ── Step 1: Basic input validation ────────────────────────
    if not college_id or not college_id.strip():
        return {"success": False, "message": "College ID cannot be empty."}

    if not password or not password.strip():
        return {"success": False, "message": "Password cannot be empty."}

    college_id = college_id.strip()

    # ── Step 2: Look up the College ID in the database ────────
    user = users_col.find_one({"college_id": college_id})

    if not user:
        # Keep the message vague — don't reveal whether the ID exists
        return {"success": False, "message": "Invalid College ID or password."}

    # ── Step 3: Verify the password ───────────────────────────
    if user["password"] != password:
        return {"success": False, "message": "Invalid College ID or password."}

    # ── Step 4: Login successful — return safe user data ──────
    # We return only the fields the app needs; we never expose
    # the raw MongoDB document (which contains the password).
    return {
        "success": True,
        "message": f"Welcome back, {user['codename']}!",
        "user": {
            "college_id" : user["college_id"],
            "codename"   : user["codename"],
            "points"     : user["points"],
            "created_at" : user["created_at"]
        }
    }