import os

STARBOARD_DATABASE = os.environ.get("STARBOARD_DATABASE", default="data/starboard.db")
STARBOARD_STATIC = os.environ.get("STARBOARD_STATIC", default="data/starboard/")
STARBOARD_KEY = os.environ.get("STARBOARD_KEY")
