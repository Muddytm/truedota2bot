import praw
import time
import td2tasks
import yaml

user = ""
password = ""


def has_replied(comment):
    """Return True if truedota2bot has already replied to this comment."""
    for reply in comment.replies:
        if reply.author.name == user:
            return True

    return False


def check_comment(comment):
    """Recursively check a comment and its replies."""
    if comment.body.startswith("!test"):
        if not has_replied(comment):
            td2tasks.test.run(comment)

    for reply in comment.replies:
        check_comment(reply)


def start():
    """Start the truedota2bot automoderator."""
    global user
    global password

    f = open("config.yml")
    config = yaml.safe_load(f)
    f.close()

    user = config["user"]
    password = config["pass"]

    reddit = praw.Reddit(user_agent="For use with /r/truedota2.")

    reddit.login(user, password, disable_warning=True)

    while True:
        subreddit = reddit.get_subreddit("mudbotdev")  # To be changed later
        for submission in subreddit.get_new(limit=100):  # 100? Maybe change
            comments = submission.comments
            for comment in comments:
                check_comment(comment)

        time.sleep(5)


if __name__ == "__main__":
    start()
