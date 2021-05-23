import time
import traceback
import praw
from praw.exceptions import RedditAPIException
from config import *


LOGIN_TRIES = 5
LOGIN_SLEEP = 5


def login():
    logging.info("Hey senpai! I'm logging in~")
    for attempt in range(LOGIN_TRIES):
        try:
            instance = praw.Reddit(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                user_agent=USER_AGENT,
                username=USERNAME,
                password=PASSWORD
            )
            logging.info("Success! I am now logged in! :D")
            return instance
        except (RedditAPIException, Exception):
            logging.warning("Hmm, something went wrong while logging in. Trying again~")
            logging.error(traceback.format_exc())
            time.sleep(LOGIN_SLEEP)
    logging.error("Sorry senpai, I was unable to log in. :(")
    return None
