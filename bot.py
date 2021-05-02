import praw
import credentials as c
import logging
import re
import sys


class Chaser:
    def __init__(self, reddit):
        self.reddit = reddit
        logging.debug("Successfully logged in!")
        self.logging_enabled = True


class Seeker:
    def __init__(self):
        logging.debug("Created a Seeker.")


if __name__ == "__main__":
    # TODO: I don't know what it does right now but I'll eventually know
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )
    logging.info("LZ CODE: 58842\nVersion 1.0 alpha\nHacking into the mainframe... ;)")

    LZ = praw.Reddit(
        client_id=c.CLIENT_ID,
        client_secret=c.CLIENT_SECRET,
        user_agent=c.USER_AGENT,
        username=c.USERNAME,
        password=c.PASSWORD
    )


