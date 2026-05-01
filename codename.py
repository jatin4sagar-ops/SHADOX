# =============================================================
# SHADOX — core/codename.py
# Generates a random anonymous codename for each user.
# A codename is one adjective + one noun joined together,
# e.g. "SilentFalcon" or "BravePanda".
# =============================================================

import random

# Import the word lists defined in config.py
from config import ADJECTIVES, NOUNS


def generate_codename():
    """
    Picks one random adjective and one random noun from the
    config lists and joins them into a single codename string.

    Returns:
        str: A codename such as "SilentFalcon".
    """

    # Step 1 — Pick a random adjective from the ADJECTIVES list
    adjective = random.choice(ADJECTIVES)

    # Step 2 — Pick a random noun from the NOUNS list
    noun = random.choice(NOUNS)

    # Step 3 — Combine both words into one PascalCase codename
    # e.g. "Silent" + "Falcon" → "SilentFalcon"
    codename = adjective + noun

    return codename