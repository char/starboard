#!/usr/bin/env python3

from starboard.env import STARBOARD_DATABASE
from starboard.db import initialise_db
import sqlite3


if __name__ == "__main__":
  db = sqlite3.connect(STARBOARD_DATABASE)
  initialise_db(db)
  db.close()
