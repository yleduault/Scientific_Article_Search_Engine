import time

import feedparser
from db import (
    clear_db,
    insert_new_paper,
    update_cross_listing,
    update_version,
    update_version_cross_listing,
)

# First clear the DB during testing
clear_db()

feeds = [
    "https://arxiv.org/rss/cs.LG",
    "https://arxiv.org/rss/cs.AI",
    "https://arxiv.org/rss/cs.CV",
    "https://arxiv.org/rss/cs.CL",
    "https://arxiv.org/rss/cs.MA",
]

for feed_url in feeds[:1]:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        # Always present elements
        link: str = str(entry["link"])
        arxiv_id: str = link.split("/")[-1]
        id: int = int("".join(arxiv_id.split(".")))
        pubDate: str = time.strftime(
            "%Y-%m-%d", time.struct_time(entry["published_parsed"])
        )
        title: str = str(entry["title"])
        tags: list = [tag["term"] for tag in entry["tags"]]
        original_tag: str = tags[0]
        tags_string: str = ",".join(tags)
        version: str = str(entry["summary"]).split(" ")[0].split("v")[-1]

        # DOI and journals if present
        if "arxiv_doi" in entry.keys():
            doi: str | None = str(entry["arxiv_doi"])
        else:
            doi = None
        if "arxiv_journal_reference" in entry.keys():
            journal: str | None = str(entry["arxiv_journal_reference"])
        else:
            journal = None
        # If revision or just new article
        match str(
            entry["arxiv_announce_type"]
        ):  # Add new paper or update. If no articles found in DB, just add it
            case "new":
                insert_new_paper(
                    id=id,
                    arxiv_id=arxiv_id,
                    url=link,
                    publication_date=pubDate,
                    title=title,
                    orig_tag=original_tag,
                    tags=tags_string,
                    doi=doi,
                    journal=journal,
                    version=version,
                )
            case "cross":
                update_cross_listing(
                    id=id,
                    arxiv_id=arxiv_id,
                    url=link,
                    publication_date=pubDate,
                    title=title,
                    orig_tag=original_tag,
                    tags=tags_string,
                    doi=doi,
                    journal=journal,
                    version=version,
                )
            case "replace":
                update_version(
                    id=id,
                    arxiv_id=arxiv_id,
                    url=link,
                    publication_date=pubDate,
                    title=title,
                    orig_tag=original_tag,
                    tags=tags_string,
                    doi=doi,
                    journal=journal,
                    version=version,
                )
            case "replace-cross":
                update_version_cross_listing(
                    id=id,
                    arxiv_id=arxiv_id,
                    url=link,
                    publication_date=pubDate,
                    title=title,
                    orig_tag=original_tag,
                    tags=tags_string,
                    doi=doi,
                    journal=journal,
                    version=version,
                )
