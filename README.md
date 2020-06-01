# Starboard

A personal link aggregator for interesting code projects / links / whatever you want.

## Motivation

I like GitHub's stars, but you can only use them on GitHub projects! Vendor lock in is sad >:(

With Starboard, you can 'star' a project from any git forge, or even any link!

## Features

- Built-in form to publish a star for an arbitrary URL.
- Publishes an RSS feed to facilitate easy following of a person's stars.
- (Should we do this server-side or let clients do it?) Periodically import stars from GitHub and GitLab

## Design

In principle, the site will be *read* much more than it is *written*, so we treat the site as
entirely static, and when the API receives an update, we regenerate the site using [sipy](https://github.com/half-cambodian-hacker-man/sipy),
my static site generator.

## Usage

The Starboard API server is configured through environment variables:
- `STARBOARD_STATIC` defines the location of the served static website. Defaults to `data/starboard/`
- `STARBOARD_DATABASE` defines the location of the sqlite3 database file. Defaults to `data/starboard.db`
- `STARBOARD_KEY` defines the authorization key to be able to modify the list of starred projects.

Starboard has one API endpoint, `/star`. You can: 
- `GET` it to list all the starred projects
- `POST` to it to add an URL / multiple URLs
- `DELETE` to remove an URL / multiple URLs.

The `POST` and `DELETE` functions require a configuration-defined key (as a `Bearer` token) in the `Authorization` header.

<!-- TODO: Example client -->
