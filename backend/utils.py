import feedparser


def retrieve_abstract(arxiv_id: int | str) -> str | None:
    if isinstance(arxiv_id, int):
        arxiv_id = str(arxiv_id)[:4] + "." + str(arxiv_id)[4:]
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}&start=0&max_results=1"
    try:
        feed = feedparser.parse(url)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    if "summary" in feed.entries[0].keys():
        return feed.entries[0]["summary"]
    return None
