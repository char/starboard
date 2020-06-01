# Build script for the static site

from starboard.db import list_starred_projects
import sqlite3
import os

def build(ctx):
  db = sqlite3.connect(os.environ["STARBOARD_DATABASE"])
  projects = list(list_starred_projects(db))
