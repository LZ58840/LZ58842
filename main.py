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


VERSION = "2.3.1"
SUBREDDIT = "Animewallpaper"


def run_mod(input_queue, output_queue):
    login_instance = login()
    time.sleep(10)
    if login_instance is not None:
        moderator = Moderator(login_instance, SUBREDDIT, SKIP_FLAGS, RULES, PRIORITY, output_queue, input_queue, False)
        logging.warning("Shadow mode is enabled by default.")
        moderator.run()
    else:
        logging.error("Unable to log in, terminating program.")
        exit(1)


def run_logger(input_queue, output_queue):
    # https://stackoverflow.com/a/51610341
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    discord_logger = LoggingClient(output_queue, input_queue)
    loop.run_until_complete(discord_logger.run(DISCORD_TOKEN))
    loop.run_forever()


if __name__ == "__main__":
    logging.basicConfig(
        filename='{}.log'.format(date.today().strftime("%d_%m_%Y")),
        filemode='a',
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )
    logging.info("LZ CODE: 58842")
    logging.info("Version %s", VERSION)

    logging_queue = Queue()
    command_queue = Queue()

    mod_thread = threading.Thread(target=run_mod, args=(command_queue, logging_queue,))
    logger_thread = threading.Thread(target=run_logger, args=(command_queue, logging_queue,))

    mod_thread.start()
    logger_thread.start()

    mod_thread.join()
    logger_thread.join()
