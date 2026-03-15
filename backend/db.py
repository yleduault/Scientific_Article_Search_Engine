import os

import psycopg

# Connect to the DB
conn = psycopg.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)


def clear_db():
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM paper_keywords;
            DELETE FROM paper_topics;
            DELETE FROM raw_keywords;
            DELETE FROM keywords;
            DELETE FROM topics;
            DELETE FROM papers;
            """)
    conn.commit()


def insert_new_paper(
    id: int,
    arxiv_id: str,
    url: str,
    publication_date: str,
    title: str,
    orig_tag: str,
    tags: str,
    doi: str | None,
    journal: str | None,
    version: str,
):
    with conn.cursor() as cur:
        # Insert into papers table
        cur.execute(
            """
            INSERT INTO papers (id,title,journal,publication_date,canonical_version,arxiv_announce_type,original_category,current_category,last_updated,url,doi,arxiv_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW()) ON CONFLICT DO NOTHING;
            """,
            (
                id,
                title,
                journal,
                publication_date,
                version,
                "new",
                orig_tag,
                tags,
                url,
                doi,
                arxiv_id,
            ),
        )

    conn.commit()


def update_cross_listing(
    id: int,
    arxiv_id: str,
    url: str,
    publication_date: str,
    title: str,
    orig_tag: str,
    tags: str,
    doi: str | None,
    journal: str | None,
    version: str,
):
    with conn.cursor() as cur:
        # Verify if the article is already recorded, if not add it

        cur.execute("""SELECT id FROM papers WHERE id=%s""", [id])
        res = cur.fetchall()
        if len(res) == 0:
            insert_new_paper(**locals())
        else:
            # Update the record into papers table
            cur.execute(
                """
                UPDATE papers SET (canonical_version=%s,arxiv_announce_type=%s,current_category=%s,last_updated=NOW())
                WHERE id = %s;
                """,
                (version, "cross", tags, id),
            )

    conn.commit()


def update_version(
    id: int,
    arxiv_id: str,
    url: str,
    publication_date: str,
    title: str,
    orig_tag: str,
    tags: str,
    doi: str | None,
    journal: str | None,
    version: str,
):
    with conn.cursor() as cur:
        # Verify if the article is already recorded, if not add it

        cur.execute("""SELECT id FROM papers WHERE id=%s""", [id])
        res = cur.fetchall()
        if len(res) == 0:
            insert_new_paper(**locals())
        else:
            # Update the record into papers table
            cur.execute(
                """
                UPDATE papers SET (canonical_version=%s,arxiv_announce_type=%s,current_category=%s,last_updated=NOW())
                WHERE id = %s;
                """,
                (version, "replace", tags, id),
            )

    conn.commit()


def update_version_cross_listing(
    id: int,
    arxiv_id: str,
    url: str,
    publication_date: str,
    title: str,
    orig_tag: str,
    tags: str,
    doi: str | None,
    journal: str | None,
    version: str,
):
    with conn.cursor() as cur:
        # Verify if the article is already recorded, if not add it

        cur.execute("""SELECT id FROM papers WHERE id=%s""", [id])
        res = cur.fetchall()
        if len(res) == 0:
            insert_new_paper(**locals())
        else:
            # Update the record into papers table
            cur.execute(
                """
                UPDATE papers SET (canonical_version=%s,arxiv_announce_type=%s,current_category=%s,last_updated=NOW())
                WHERE id = %s;
                """,
                (version, "replace-cross", tags, id),
            )

    conn.commit()
