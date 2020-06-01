import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit

from starboard.db import StarredProject


USER_AGENT = "Starboard (https://github.com/half-cambodian-hacker-man/starboard)"


def parse_opengraph(doc):
  opengraph_tags = {}

  ogs = doc.html.head.findAll(property=re.compile(r"^og"))
  for og in ogs:
    opengraph_tags[og["property"][3:]] = og["content"]


def og_valid(og):
  required_attrs = ["title", "type", "image", "url"]
  return all([hasattr(og, attr) for attr in required_attrs])


def scrape_project_info(url) -> StarredProject:
  r = requests.get(url, headers={ "User-Agent": USER_AGENT })
  bs = BeautifulSoup(r.text)

  hostname = urlsplit(url)[1]

  title = bs.title.string
  description = hostname

  og = parse_opengraph(html=bs)
  if og_valid(og):
    if "description" in og:
      description = og["description"]
      title = og["title"] + " @ " + og.get("site_name", default=hostname)
    else:
      title = og["title"]

  return StarredProject(0, url, title, description, None)
