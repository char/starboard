import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import re

from starboard.db import StarredProject


USER_AGENT = "Starboard (https://github.com/half-cambodian-hacker-man/starboard)"


def parse_opengraph(doc):
    opengraph_tags = {}

    ogs = doc.html.head.findAll(property=re.compile(r"^og"))
    for og in ogs:
        opengraph_tags[og["property"][3:]] = og["content"]

    return opengraph_tags


def og_valid(og):
    required_attrs = ["title"]
    return all(attr in og for attr in required_attrs)


def scrape_project_info(url) -> StarredProject:
    r = requests.get(url, headers={"User-Agent": USER_AGENT})
    bs = BeautifulSoup(r.text, features="html.parser")

    hostname = urlsplit(url)[1]

    title = bs.title.string
    description = hostname

    og = parse_opengraph(doc=bs)
    if og_valid(og):
        if "description" in og:
            description = og["description"]
            description = remove_suffix(description, og["title"]).rstrip("- :")
            description = remove_suffix(
                description,
                ". Contribute to "
                + og["title"]
                + " development by creating an account on GitHub.",
            )

            title = og["title"] + " @ " + og.get("site_name", hostname)
        else:
            title = og["title"]

    return StarredProject(0, url, title, description, None, None)


def remove_suffix(s: str, suffix: str, /) -> str:
    if suffix and s.endswith(suffix):
        return s[: -len(suffix)]
    else:
        return s[:]
