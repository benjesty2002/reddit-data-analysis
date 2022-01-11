# adapted from https://gist.github.com/jamescalam/d7e6a7236e99369123237f0ba371da18#file-reddit-oauth-py

import requests
import json


class RedditScraper:

    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.headers = self.get_auth_headers()

    def get_auth_headers(self):
        # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
        with open(self.config_file, "r") as f:
            config = json.load(f)
        auth = requests.auth.HTTPBasicAuth(config["access_key"], config["secret_key"])

        # here we pass our login method (password), username, and password
        data = {
            "grant_type": "password",
            "username": config["username"],
            "password": config["password"]
        }
        # setup our header info, which gives reddit a brief description of our app
        headers = {"User-Agent": f"{config['botname']}/{config['botversion']}"}

        # send our request for an OAuth token
        res = requests.post("https://www.reddit.com/api/v1/access_token",
                            auth=auth, data=data, headers=headers)

        # convert response to JSON and pull access_token value
        access_token = res.json()["access_token"]

        # add authorization to our headers dictionary
        headers = {**headers, "Authorization": f"bearer {access_token}"}

        return headers

    def get(self, url, **kwargs):
        print(url)
        kwargs["headers"] = self.headers
        try:
            return requests.get(url, **kwargs)
        except requests.RequestException:
            self.headers = self.get_auth_headers()
            return requests.get(url, **kwargs)

    def get_posts(self, subreddit, **kwargs):
        resp = self.get(f"https://oauth.reddit.com/r/{subreddit}", **kwargs)
        return resp.json()["data"]["children"]

    def get_comments(self, subreddit, post_id, **kwargs):
        resp = self.get(f"https://oauth.reddit.com/r/{subreddit}/comments/{post_id}", **kwargs).json()
        post = resp[0]["data"]
        comments = self._child_comment(resp[1])
        return comments, post

    @staticmethod
    def _child_comment(replies):
        if replies == "":
            return None
        return [
            {
                "author": child["data"].get("author"),
                "comment": child["data"].get("body"),
                "upvotes": child["data"].get("ups"),
                "downvotes": child["data"].get("downs"),
                "replies": RedditScraper._child_comment(child["data"].get("replies", ""))
            }
            for child in replies["data"]["children"]
        ]

if __name__ == '__main__':
    rs = RedditScraper()
    posts = rs.get_posts("python/new")

    print(json.dumps(posts, indent=4))
