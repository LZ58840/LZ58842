from evaluator import Evaluator
from abc import ABC
import re
from search_exp import RESOLUTION_ANY


class ResolutionAny(Evaluator, ABC):
    def __init__(self, post):
        super().__init__(post, self.__class__.__name__)
        self.width = 0
        self.height = 0

    def evaluate(self):
        resolution = re.search(RESOLUTION_ANY, self.post.title)
        return resolution is not None

    def to_string(self):
        return 3, "**unable to detect a resolution in title**, " \
               "ensure resolution is formatted as <width>x<height> " \
               "**in (round) or [square] brackets**"


class ImageEvaluator(Evaluator, ABC):
    def __init__(self, post):
        super().__init__(post, self.__class__.__name__)
        self.image_resolution = None
        self.title_resolution = None

    def get_title(self):
        resolution = re.search(RESOLUTION_ANY, self.post.title)
        if resolution is not None:
            self.title_resolution = (resolution.group(1), resolution.group(2))
        pass

    def get_image(self):
        pass