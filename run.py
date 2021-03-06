import praw
import random
import time
import td2tasks
import yaml

author = ""
user = ""
password = ""
jokes = ["Hoho, haha! ", "Zip! Zap! ", "Beep boop, ", "Meep merp, ", "Waow! "]


def send_reply(text, comment):
    """Reply to a command."""
    if text and text != "":
        text += "\n\n--------\n\n"
        joke = jokes[random.randint(0, len(jokes) - 1)]
        text += "^(" + joke + "I'm a bot!) [^(Message my author)](http://www.reddit.com/message/compose/?to=" + author + ") ^(if you have any suggestions or bugs to report, and) [^(check me out on Github!)](https://github.com/Muddytm/truedota2bot) ^(if you like that sort of thing.)"
        comment.reply(text)


def has_replied(comment):
    """Return True if truedota2bot has already replied to this comment."""
    time.sleep(1)
    for reply in comment.replies:
        if reply.author.name.lower() == user.lower():
            return True

    return False


def check_comment(comment):
    """Recursively check a comment and its replies."""
    text = comment.body

    if "!patchnotes" in text.strip():
        if not has_replied(comment):
            send_reply(td2tasks.patchnotes.run(text), comment)

    if "!teamsummary" in comment.body.strip():
        if not has_replied(comment):
            send_reply(td2tasks.newteamsummary.run(text), comment)

    for reply in comment.replies:
        try:
            check_comment(reply)
        except AttributeError:
            pass


def start():
    """Start the truedota2bot automoderator."""
    global user
    global password

    f = open("config.yml")
    config = yaml.safe_load(f)
    f.close()

    author = config["author"]
    user = config["user"]
    password = config["pass"]
    sub = config["sub"]

    reddit = praw.Reddit(user_agent="For use with /r/truedota2.")

    reddit.login(user, password, disable_warning=True)

    while True:
        try:
            subreddit = reddit.get_subreddit(sub)
            for submission in subreddit.get_new(limit=50):  # Arbitrary
                comments = submission.comments
                for comment in comments:
                    try:
                        check_comment(comment)
                    except AttributeError:
                        pass
        except praw.errors.HTTPException:
            print ("Ran into an error?")


if __name__ == "__main__":
    start()
