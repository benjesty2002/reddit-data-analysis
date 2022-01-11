from reddit_reader import RedditScraper


def latest_posts(subreddit, limit=100, before=None):
    rs = RedditScraper()
    params = {"limit": limit}
    if before is not None:
        params["before"] = before
    url = f"https://oauth.reddit.com/r/{subreddit}/new"

    while True:
        posts = rs.get_posts(subreddit, params=params)
        while len(posts) > 0:
            post = posts.pop(-1)
            post["full_id"] = post['kind'] + '_' + post["data"]['id']
            params["before"] = post["full_id"]
            yield post
        yield None
