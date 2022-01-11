import json

from reddit_reader import RedditScraper
from subreddit_generators import latest_posts
from datetime import datetime
from time import sleep

rs = RedditScraper()
comments, _ = rs.get_comments("dataisbeautiful", "s0mo4d")
with open("comments.json", "w+") as f:
    json.dump(comments, f, indent=4)
#
# posts = latest_posts("python/hot", limit=1)
#
# for post in posts:
#     if post is None:
#         print("no new posts, sleeping")
#         sleep(5)
#     else:
#         dt = datetime.fromtimestamp(post["data"]["created_utc"])
#         print()
#         comments, _ = rs.get_comments("python", post["data"]["id"])
#         # print(json.dumps(comments, indent=4))
#         print(post["data"]["id"])
#         print(dt.strftime("%H:%M:%S"))
#         with open("comments.json", "w+") as f:
#             json.dump(comments, f, indent=4)
#         sleep(60)
