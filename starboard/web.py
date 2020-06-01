#!/usr/bin/env python3

from starboard.db import STARRED_PROJECTS_TABLE, list_starred_projects, add_project
from starboard.env import STARBOARD_KEY, STARBOARD_DATABASE
from starboard.scraping import scrape_project_info

from flask import Flask, request, jsonify, g
import sqlite3


app = Flask(__name__)


def get_db() -> sqlite3.Connection:
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect(STARBOARD_DATABASE)
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()


def list_stars():
  db = get_db()

  result = []
  for proj in list_starred_projects(db):
    result.append({
      "url": proj.url,
      "title": proj.title,
      "description": proj.description,
      "note": proj.note,
      "date": proj.timestamp
    })

  return jsonify(result)


@app.route("/star", methods=["GET", "POST", "DELETE"])
def star():
  if request.method == "GET":
    return list_stars()

  urls = None
  notes = None
  if request.is_json():
    body = request.get_json()
    urls = body.get("urls")
    notes = body.get("notes")
  else:
    urls = request.form.getlist("urls[]")
    notes = request.form.getlist("notes[]")

  if not urls:
    return jsonify({ "error": "Missing request body" }), 400

  if request.headers.get("Authorization") != STARBOARD_KEY:
    return jsonify({ "error": "Invalid value for Authorization header" }), 403

  urls = body["urls"]
  if urls is None or type(urls) != list:
    return jsonify({ "error": "Invalid or missing parameter 'urls'" }), 400

  db = get_db()
  c = db.cursor()
  if request.method == "DELETE":
    c.executemany(f"DELETE FROM {STARRED_PROJECTS_TABLE} WHERE url = ?", )
    rebuild_site()

    return jsonify(urls), 200

  projects = [scrape_project_info(url) for url in urls]

  if notes:
    for idx, note in enumerate(notes):
      if note:
        projects[idx].note = note

  for project in projects:
    add_project(db, project)
  rebuild_site()

  return jsonify(projects)
