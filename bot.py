import time
import praw
import credentials as c
import subreddits as s
import logging
from resolution_any import ResolutionAny
from resolution_bad import ResolutionBad
from aspect_ratio_bad import AspectRatioBad
from resolution_mismatch import ResolutionMismatch
from comment import RemoveComment
import sys

LIMIT = 5
REFRESH = 60
VERSION = "1.0 alpha 2"
SIGNATURE = "\n\n*I am a bot, and this action was performed automatically at the request of my senpai, u/LZ58840.*"


def remove_post(post, comment):
    comment = post.reply(comment.to_string() + SIGNATURE)
    comment.mod.distinguish(sticky=True)
    post.mod.lock()
    post.mod.remove()


class Chaser:
    def __init__(self, reddit, subreddit):
        self.reddit = reddit
        self.subreddit = subreddit
        self.logging_enabled = True
        self.visited = []
        logging.debug("Successfully logged in!")

    def mod_queue_handler(self, sub):
        logging.debug("Checking posts from %s...", sub)
        print("===== UNMODERATED =====")  # FOR TEST PURPOSES
        for post in self.reddit.subreddit(sub).mod.unmoderated(limit=LIMIT):
            if post.id not in self.visited:
                if len(self.visited) == 100:
                    self.visited.pop(0)
                self.visited.append(post.id)
            else:
                continue
            if post.selftext != "" or post.link_flair_text not in ["Desktop", "Mobile"]:
                continue
            # FOR TEST PURPOSES
            print(post.title)
            print(post.author)
            print(post.created_utc)
            print(post.permalink)
            print(post.url)
            print(post.link_flair_text)
            print()

            removal_comment = RemoveComment()

            for evaluator in [ResolutionAny, ResolutionBad, AspectRatioBad, ResolutionMismatch]:
                curr = evaluator(post)
                rule, content = curr.check()
                if rule is not None:
                    removal_comment.add_violation(rule, content)
                    if evaluator == ResolutionAny:
                        break

            if not removal_comment.is_empty():
                remove_post(post, removal_comment)
        return

    def run(self):
        while True:
            logging.debug("Checking posts...")
            try:
                self.mod_queue_handler(s.TEST)
            except Exception as e:
                logging.exception(e)
            logging.debug("Operations completed. Refreshing in {} seconds...".format(REFRESH))
            time.sleep(REFRESH)


class Seeker:
    def __init__(self):
        logging.debug("Created a Seeker.")


if __name__ == "__main__":
    logging.basicConfig(

        stream=sys.stdout,
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s: %(message)s"
    )
    logging.info("\nLZ CODE: 58842")
    logging.info("Version {}".format(VERSION))
    logging.info("\nHey, senpai! I'm logging in...")

    LZ = Chaser(
        praw.Reddit(
            client_id=c.CLIENT_ID,
            client_secret=c.CLIENT_SECRET,
            user_agent=c.USER_AGENT,
            username=c.USERNAME,
            password=c.PASSWORD
        ),
        s.TEST
    )

    LZ.run()
