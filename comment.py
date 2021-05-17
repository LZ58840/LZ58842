import logging
from abc import abstractmethod, ABC

# Moderator comment constants.
SIGNATURE = "\n*I am a bot, and this action was performed automatically at the request of my senpai, u/LZ58840.* "


class Comment:
    def __init__(self):
        self.body = ""

    @abstractmethod
    def add(self, *args):
        pass

    @abstractmethod
    def update(self, *args):
        pass

    def is_empty(self):
        self.update()
        return self.body == ""

    def to_string(self):
        self.update()
        return self.body


class RemovalComment(Comment, ABC):
    def __init__(self):
        super().__init__()
        self.violations = {}

    def add(self, rule, comment):
        if rule in self.violations:
            self.violations[rule] += ", " + comment
        else:
            self.violations[rule] = comment

    def update(self):
        self.body = ""
        if len(self.violations) > 0:
            self.body = "removed, "
            for rule in self.violations.keys():
                self.body += "rule " + str(rule) + ": "
                self.body += self.violations[rule]
                self.body += ".\n\n; "
            self.body = self.body.rstrip("; ")
