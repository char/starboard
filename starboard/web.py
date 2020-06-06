#!/usr/bin/env python3

from starboard.db import STARRED_PROJECTS_TABLE, list_starred_projects, add_project
from starboard.env import STARBOARD_KEY, STARBOARD_DATABASE
from starboard.scraping import scrape_project_info
from starboard.building import rebuild_site

from flask import Flask, request, jsonify, g, redirect, Response
import sqlite3


app = Flask(__name__, static_folder="../static_out", static_url_path="")


@app.before_first_request
def build_on_start():
  rebuild_site()


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

  key = None
  urls = None
  notes = None
  if request.is_json:
    body = request.get_json()
    key = body.get("key")
    urls = body.get("urls")
    notes = body.get("notes")
  else:
    key = request.form.get("key")
    urls = request.form.getlist("urls[]")
    notes = request.form.getlist("notes[]")

  if not urls:
    return jsonify({ "error": "Missing request body" }), 400

  if key is None:
    key = request.headers.get("Authorization")

  if key != STARBOARD_KEY:
    return jsonify({ "error": "Invalid key value" }), 403

  if urls is None or type(urls) != list:
    return jsonify({ "error": "Invalid or missing parameter 'urls'" }), 400

  db = get_db()
  c = db.cursor()
  if request.method == "DELETE":
    c.executemany(f"DELETE FROM {STARRED_PROJECTS_TABLE} WHERE url = ?", )
    rebuild_site()

    return jsonify(urls), 200

  if not all(url.startswith("http://") or url.startswith("https://") for url in urls):
    return jsonify({ "error": "All URLs must be of the HTTP or HTTPS scheme." }), 400

  projects = [scrape_project_info(url) for url in urls]

  if notes:
    for idx, note in enumerate(notes):
      if note:
        projects[idx].note = note

  projects = [add_project(db, project) for project in projects]
  rebuild_site()

  if "redir" in request.args:
    return redirect("/")

  res = Response()
  res.status_code = 304
  res.headers["Location"] = "/"
  res.autocorrect_location_header = False
  return res

@app.route("/")
def index_page():
  return app.send_static_file("index.html")

@app.route("/star/")
def star_index_page():
  return app.send_static_file("star/index.html")
