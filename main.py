import logging
import sys
from moderator import Moderator
from login import login
from skip_flags import SKIP_FLAGS
from config import RULES, PRIORITY

VERSION = "2.0 alpha"
SUBREDDIT = "LZ58840"

if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )
    logging.info("\nLZ CODE: 58842")
    logging.info("Version %s", VERSION)

    login_instance = login()

    if login_instance is not None:
        moderator = Moderator(login_instance, SUBREDDIT, SKIP_FLAGS, RULES, PRIORITY)
        moderator.run()
    else:
        logging.error("Unable to log in, terminating program.")
