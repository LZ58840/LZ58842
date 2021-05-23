import logging
import threading
from datetime import date
import asyncio
import time
from queue import Queue
from moderator import Moderator
from login import login
from skip_flags import SKIP_FLAGS
from config import RULES, PRIORITY, DISCORD_TOKEN
from discord_logging import LoggingClient


VERSION = "2.1 beta"
SUBREDDIT = "Animewallpaper"


def run_mod(logging_queue):
    login_instance = login()
    time.sleep(10)
    if login_instance is not None:
        moderator = Moderator(login_instance, SUBREDDIT, SKIP_FLAGS, RULES, PRIORITY, logging_queue, True)
        moderator.run()
    else:
        logging.error("Unable to log in, terminating program.")
        exit(1)


def run_logger(logging_queue):
    asyncio.set_event_loop(asyncio.new_event_loop())
    discord_logger = LoggingClient(logging_queue)
    discord_logger.run(DISCORD_TOKEN)


if __name__ == "__main__":
    logging.basicConfig(
        filename='{}.log'.format(date.today().strftime("%d_%m_%Y")),
        filemode='a',
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )
    logging.info("LZ CODE: 58842")
    logging.info("Version %s", VERSION)

    comm_queue = Queue()
    mod_thread = threading.Thread(target=run_mod, args=(comm_queue,))
    logger_thread = threading.Thread(target=run_logger, args=(comm_queue,))

    mod_thread.start()
    logger_thread.start()

    mod_thread.join()
    logger_thread.join()
