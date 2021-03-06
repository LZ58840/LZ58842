import logging
import time
from comment import SIGNATURE, RemovalComment

# Moderation queue constants.
LIMIT = 10
REFRESH = 60
DISCORD_SHADOW = "!shadow"


def create_action(submission, comment):
    return {
        "common": "removal",
        "title": submission.title,
        "author": submission.author.name,
        "type": submission.link_flair_text,
        "permalink": submission.shortlink,
        "comment": comment.to_string()
    }


class Moderator:
    def __init__(self, reddit, subreddit, skip_flags, rules, priority, logging_queue, command_queue, shadow_mode):
        self.reddit = reddit
        self.subreddit = subreddit
        self.skip_flags = skip_flags
        self.rules = rules
        self.priority_rules = [rules[index] for index in priority]
        self.visited = []
        self.logging_enabled = True
        self.logging_queue = logging_queue
        self.command_queue = command_queue
        self.counter = 1
        self.shadow_mode = shadow_mode
        logging.debug("%s object created.", self.__class__.__name__)

    def remove_submission(self, submission, removal_comment):
        if self.shadow_mode:
            logging.warning("Shadow mode is enabled, no real action will be taken.")
        else:
            logging.debug("Removing post %s...", submission.id)
            comment = submission.reply(removal_comment.to_string() + SIGNATURE)
            comment.mod.distinguish(sticky=True)
            submission.mod.lock()
            submission.mod.remove()
        logging.info("---------- ACTION WAS TAKEN ----------")
        logging.info("Submission %s was removed:\n\n%s", submission.id, removal_comment.to_string())

    def has_visited(self, submission):
        if submission.id not in self.visited:
            if len(self.visited) == LIMIT:
                self.visited.pop(0)
            self.visited.append(submission.id)
            return False
        return True

    def can_skip(self, submission):
        result = False
        for flag in self.skip_flags:
            result |= flag(submission)
        return result

    def submission_details(self, submission):
        logging.info("---------- SUBMISSION #%d ----------", self.counter)
        logging.debug("Submission ID: %s", submission.id)
        logging.info("Title: %s", str(submission.title.encode("ascii", "ignore")).rstrip("'").lstrip("b'")),
        logging.info("Author: %s", submission.author.name)
        logging.info("Type: %s", submission.link_flair_text)
        logging.debug("Created: %s", submission.created_utc)
        logging.debug("Permalink: %s", submission.permalink)
        logging.debug("URL: %s \n", submission.url)

    def rule_handler(self, submission):
        removal_comment = RemovalComment()
        for rule in self.rules:
            evaluating_submission = rule(submission)
            violation = evaluating_submission.check()
            if violation is not None:
                removal_comment.add(evaluating_submission.get_rule(), violation)
                if rule in self.priority_rules:
                    break
        return removal_comment

    def queue_handler(self):
        self.counter = 1
        logging.debug("Checking latest %d submissions from %s...", LIMIT, self.subreddit)
        for submission in self.reddit.subreddit(self.subreddit).mod.unmoderated(limit=LIMIT):
            if self.has_visited(submission) or self.can_skip(submission):
                continue
            self.submission_details(submission)
            removal_comment = self.rule_handler(submission)
            if not removal_comment.is_empty():
                self.remove_submission(submission, removal_comment)
                self.logging_queue.put(create_action(submission, removal_comment))
            self.counter += 1

    def shadow_switch(self, switch):
        self.shadow_mode = switch != "enable"

    def command_handler(self):
        if not self.command_queue.empty():
            command = self.command_queue.get().split(" ")
            if command[0].startswith(DISCORD_SHADOW):
                self.shadow_switch(command[1])
                msg = "Shadow mode has been {}.".format(command[1] + "d")
                logging.info(msg)
                self.logging_queue.put(msg)

    def run(self):
        while True:
            logging.debug("Refreshing...")
            try:
                self.queue_handler()
                self.command_handler()
            except Exception as e:
                logging.exception(e)
            logging.debug("Operations completed. Refreshing in {} seconds...".format(REFRESH))
            time.sleep(REFRESH)

