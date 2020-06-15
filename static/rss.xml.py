from datetime import datetime


def project_rss(star_id, project):
    return f"""
    <item>
        <guid>https://stars.hackery.site/star-{star_id}</guid>
        <link>https://stars.hackery.site/star-{star_id}</link>
        <pubDate>{project.timestamp}</pubDate>
        <title>{project.title}<title>
        <description>{project.description}</description>
    </item>"""


def render_text(ctx, projects):
    generation_date = datetime.now().isoformat()

    return f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
    <channel>
        <title>Starboard</title>
        <description>Link aggregator for interesting code projects</description>
        <lastBuildDate>{generation_date}</lastBuildDate>
        {''.join(map(project_rss, projects))}
    </channel>
</rss>"""
