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
SIGNATURE = "\n\n*I am a bot, and this action was performed automatically at the request of my master, u/LZ58840.*"


def remove_post(post, comment):
    comment = post.reply(comment.to_string() + SIGNATURE)
    comment.mod.distinguish(sticky=True)
    post.mod.lock()
    post.mod.remove()


class Chaser:
    def __init__(self, reddit):
        self.reddit = reddit
        logging.debug("Successfully logged in!")
        self.logging_enabled = True

    def mod_queue_handler(self, sub):
        logging.debug("Checking posts from %s...", sub)
        print("===== UNMODERATED =====")  # FOR TEST PURPOSES
        for post in self.reddit.subreddit(sub).mod.unmoderated(limit=LIMIT):
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
            logging.debug("Will check again in 1 minute...")
            time.sleep(60)


class Seeker:
    def __init__(self):
        logging.debug("Created a Seeker.")


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )
    logging.info("\nLZ CODE: 58842\nVersion 1.0 alpha\n\nHacking into the mainframe... ;)")

    LZ = Chaser(
            praw.Reddit(
                client_id=c.CLIENT_ID,
                client_secret=c.CLIENT_SECRET,
                user_agent=c.USER_AGENT,
                username=c.USERNAME,
                password=c.PASSWORD
            )
        )

    LZ.run()




