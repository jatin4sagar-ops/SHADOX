# =============================================================
# SHADOX — core/chat.py
# Handles sending and retrieving chat messages.
# All messages are stored in the MongoDB `messages` collection.
# =============================================================

from datetime import datetime

# Import the messages collection
from db.db import messages_col

# Import chat-related constants
from config import MAX_MESSAGE_LENGTH, MESSAGES_TO_DISPLAY

# Add these 👇
from core.points import add_points
from core.streaks import update_streak

# ── Send message ──────────────────────────────────────────────

def send_message(codename, text):
    """
    Validates and stores a new chat message in MongoDB.

    Steps:
        1. Check that the message is not blank.
        2. Trim the message if it exceeds MAX_MESSAGE_LENGTH.
        3. Build the message document with a timestamp.
        4. Insert it into the `messages` collection.
        5. Return a success or error result.

    Args:
        codename (str): The sender's anonymous codename, e.g. "SilentFalcon".
        text     (str): The message content typed by the user.

    Returns:
        dict: {
            "success": bool,
            "message": str   ← human-readable result description
        }
    """

    # ── Step 1: Make sure the message is not empty ────────────
    if not text or not text.strip():
        return {"success": False, "message": "Message cannot be empty."}

    if not codename or not codename.strip():
        return {"success": False, "message": "Codename is missing. Please log in again."}

    # Remove leading/trailing whitespace
    text = text.strip()

    # ── Step 2: Enforce the maximum message length ────────────
    # If the user typed more than MAX_MESSAGE_LENGTH characters,
    # silently trim it rather than rejecting the whole message.
    if len(text) > MAX_MESSAGE_LENGTH:
        text = text[:MAX_MESSAGE_LENGTH]

    # ── Step 3: Build the message document ───────────────────
    message_document = {
        "codename"  : codename,        # Who sent it (anonymous codename only)
        "text"      : text,            # The message content
        "timestamp" : datetime.now()   # Exact time the message was sent
    }

    # ── Step 4: Insert into MongoDB ───────────────────────────
    try:
        messages_col.insert_one(message_document)
        # Add points
        add_points(codename)

        # Update streak 🔥
        update_streak(codename)

        return {"success": True, "message": "Message sent."}
    except Exception as e:
        return {"success": False, "message": f"Failed to send message: {str(e)}"}

# ── Get recent messages ───────────────────────────────────────

def get_recent_messages():
    """
    Fetches the most recent messages from MongoDB, sorted oldest
    to newest so they display in natural reading order.

    Steps:
        1. Query the `messages` collection.
        2. Sort by timestamp — newest first (so we grab the right ones).
        3. Limit the results to MESSAGES_TO_DISPLAY.
        4. Reverse the list so the oldest of the batch appears at the top.
        5. Return the list, or an empty list if something goes wrong.

    Returns:
        list[dict]: A list of message dicts, each containing:
                    {
                        "codename"  : str,
                        "text"      : str,
                        "timestamp" : datetime
                    }
                    Returns [] on error.
    """

    try:
        # ── Step 2 & 3: Query MongoDB ─────────────────────────
        # Sort by timestamp descending (-1) so the most recent
        # messages come first, then limit to MESSAGES_TO_DISPLAY.
        cursor = (
            messages_col
            .find(
                {},                          # No filter — fetch all messages
                {"_id": 0,                   # Exclude the internal MongoDB ID
                 "codename"  : 1,
                 "text"      : 1,
                 "timestamp" : 1}
            )
            .sort("timestamp", -1)           # Newest first
            .limit(MESSAGES_TO_DISPLAY)      # Cap the result count
        )

        # Convert the cursor to a plain Python list
        messages = list(cursor)

        # ── Step 4: Reverse so oldest message appears at top ──
        # Example: if we fetched messages 41-50, we want 41 at
        # the top of the chat window and 50 at the bottom.
        messages.reverse()

        return messages

    except Exception as e:
        # Return an empty list so the GUI doesn't crash on a DB error
        print(f"[SHADOX] Error fetching messages: {str(e)}")
        return []