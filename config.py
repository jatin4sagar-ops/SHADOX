# =============================================================
# SHADOX — config.py
# Central configuration file.
# Import constants from here instead of hardcoding them
# anywhere else in the project.
# =============================================================


# ── MongoDB ───────────────────────────────────────────────────

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME   = "shadox_db"


# ── App info ──────────────────────────────────────────────────

APP_NAME    = "SHADOX"
APP_VERSION = "1.0.0"


# ── Points system ─────────────────────────────────────────────
# How many points a user earns per action.

POINTS_PER_MESSAGE  = 5   # Awarded each time a user sends a message
POINTS_PER_REGISTER = 10  # Bonus points on first registration


# ── Chat settings ─────────────────────────────────────────────

MAX_MESSAGE_LENGTH  = 300   # Max characters allowed per message
CHAT_REFRESH_MS     = 3000  # How often the chat window polls for new messages (milliseconds)
MESSAGES_TO_DISPLAY = 50    # How many recent messages to load at once


# ── Codename generator ────────────────────────────────────────
# A random adjective + noun is combined to create each user's
# anonymous codename, e.g. "SilentFalcon" or "BravePanda".
# Add more words to either list to increase variety.

ADJECTIVES = [
    "Silent",
    "Brave",
    "Clever",
    "Swift",
    "Calm",
    "Bold",
    "Fierce",
    "Gentle",
    "Mighty",
    "Witty",
    "Proud",
    "Eager",
    "Lucky",
    "Quirky",
    "Rapid",
    "Shiny",
    "Sneaky",
    "Sparky",
    "Sturdy",
    "Vivid",
    "Fuzzy",
    "Groovy",
    "Humble",
    "Jolly",
    "Nimble",
]

NOUNS = [
    "Falcon",
    "Panda",
    "Tiger",
    "Wolf",
    "Eagle",
    "Shark",
    "Lynx",
    "Raven",
    "Cobra",
    "Bison",
    "Otter",
    "Gecko",
    "Moose",
    "Viper",
    "Koala",
    "Dingo",
    "Hyena",
    "Lemur",
    "Tapir",
    "Bison",
    "Crane",
    "Finch",
    "Heron",
    "Quail",
    "Trout",
]