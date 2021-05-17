import logging
from abc import abstractmethod


class Evaluator:
    def __init__(self, submission, name):
        self.submission = submission
        logging.debug("Successfully created a %s Evaluator for submission %s.", name, submission.name)

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def to_string(self, *args):
        pass

    def check(self):
        if not self.evaluate():
            return self.to_string()
        return None
