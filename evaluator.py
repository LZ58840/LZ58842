import logging
from abc import abstractmethod


class Evaluator:
    def __init__(self, post, name):
        self.post = post
        logging.debug("Successfully created a {} Evaluator for post {}".format(name, post.name))
        self.logging_enabled = True

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def to_string(self, *args):
        pass

    def check(self):
        if not self.evaluate():
            return self.to_string()
        return None, None
