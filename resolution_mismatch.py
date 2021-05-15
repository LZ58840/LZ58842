import re

from resolution_bad import ResolutionBad
from search_exp import RESOLUTION_ANY


class ResolutionMismatch(ResolutionBad):
    def __init__(self, post):
        super().__init__(post)
        resolution = re.search(RESOLUTION_ANY, self.post.title)
        self.title_width, self.title_height = int(resolution.group(1)), int(resolution.group(2))

    def evaluate(self):
        return self.width == self.title_width and self.height == self.title_height

    def to_string(self):
        return 3, "**misleading** resolution in title (*claimed* {}x{}, *actual* **{}x{}**)".format(
            self.title_width, self.title_height,
            self.width, self.height
        )
