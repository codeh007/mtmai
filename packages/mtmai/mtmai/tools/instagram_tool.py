from smolagents import Tool

from mtmai.mtlibs.instagrapi import Client


class InstagramLoginTool(Tool):
    name = "instagram_login"
    description = """登录 instagram
    """
    inputs = {
        "task": {
            "type": "string",
            "description": "the task category (such as text-classification, depth-estimation, etc)",
        }
    }
    output_type = "string"

    def forward(self, task: str):
        IG_USERNAME = ""
        IG_PASSWORD = ""
        IG_CREDENTIAL_PATH = "./ig_settings.json"
        # SLEEP_TIME = "600"  # in seconds

        ig_client = Client()
        ig_client.login(IG_USERNAME, IG_PASSWORD)
        ig_client.dump_settings(IG_CREDENTIAL_PATH)

        userid = ig_client.user_id_from_username("hello")
        ig_client.user_follow(userid)
        ig_client.user_unfollow(userid)
        ig_client.user_followers(userid, amount=10)
        ig_client.user_following(userid, amount=10)
        ig_client.user_followers_full(userid, amount=10)
