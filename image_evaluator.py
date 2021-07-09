import logging
import re
import shutil
import requests
from PIL import Image
from evaluator import Evaluator
from abc import ABC


FLAIR_MOBILE = "Mobile"
FLAIR_DESKTOP = "Desktop"
RESOLUTION_ANY = r"[(\[]\s?([0-9]{3,})\s?[Xx×]\s?([0-9]{3,})\s?[)\]]"
RESOLUTION_MIN = {FLAIR_MOBILE: [900, 1600], FLAIR_DESKTOP: [1920, 1080]}
ASPECT_RATIO = {FLAIR_MOBILE: 0.625, FLAIR_DESKTOP: 1.6}


class ImageEvaluator(Evaluator, ABC):
    def __init__(self, submission, name, rule):
        super().__init__(submission, name)
        self.image_resolution = self.get_image()
        self.title_resolution = self.get_title()
        self.type = submission.link_flair_text
        self.rule = rule

    def get_title(self):
        resolution = re.search(RESOLUTION_ANY, self.submission.title)
        if resolution is not None:
            return int(resolution.group(1)), int(resolution.group(2))

    def get_rule(self):
        return self.rule

    def get_image(self):
        get_img = requests.get(self.submission.url, stream=True)
        if get_img.status_code == 200:
            get_img.raw.decode_content = True
            with open("../../img", 'wb') as img:
                shutil.copyfileobj(get_img.raw, img)
            img.close()
            image = Image.open("../../img")
            return image.size
        else:
            logging.error("Image could not be retrieved.")


class ResolutionAny(ImageEvaluator, ABC):
    def __init__(self, submission):
        super().__init__(submission, self.__class__.__name__, 3)

    def evaluate(self):
        return self.title_resolution is not None

    def to_string(self):
        return "**unable to detect a resolution in title**, " \
               "ensure resolution is formatted as <width>x<height> " \
               "**in (round) or [square] brackets**"


class ResolutionBad(ImageEvaluator, ABC):
    def __init__(self, submission):
        super().__init__(submission, self.__class__.__name__, 2)

    def evaluate(self):
        return self.image_resolution[0] >= RESOLUTION_MIN[self.type][0] \
               and self.image_resolution[1] >= RESOLUTION_MIN[self.type][1]

    def to_string(self):
        return "**resolution** of {} wallpaper must be **minimum {}x{}**".format(
            self.submission.link_flair_text.lower(),
            RESOLUTION_MIN[self.type][0],
            RESOLUTION_MIN[self.type][1]
        )


class AspectRatioBad(ImageEvaluator, ABC):
    def __init__(self, submission):
        super().__init__(submission, self.__class__.__name__, 2)
        self.aspect_ratio = round(self.image_resolution[0] / self.image_resolution[1], 3)

    def evaluate(self):
        if self.type == FLAIR_MOBILE:
            return self.aspect_ratio <= ASPECT_RATIO[FLAIR_MOBILE]
        elif self.type == FLAIR_DESKTOP:
            return self.aspect_ratio >= ASPECT_RATIO[FLAIR_DESKTOP]

    def to_string(self):
        body = ""
        if self.type == FLAIR_MOBILE:
            body += " (W/H {0} or less)**\n\nyour aspect ratio (W/H): **{1}** (> {0}, too wide)".format(
                ASPECT_RATIO[FLAIR_MOBILE],
                self.aspect_ratio
            )
        elif self.type == FLAIR_DESKTOP:
            body += " (W/H {0} or more)**\n\nyour aspect ratio (W/H): **{1}** (< {0}, too tall)".format(
                ASPECT_RATIO[FLAIR_DESKTOP],
                self.aspect_ratio
            )
        return "**aspect ratio** of {} wallpaper **must be proper".format(self.type.lower()) + body


class ResolutionMismatch(ImageEvaluator, ABC):
    def __init__(self, submission):
        super().__init__(submission, self.__class__.__name__, 3)

    def evaluate(self):
        return self.title_resolution == self.image_resolution

    def to_string(self):
        return "**misleading** resolution in title (*claimed* {}x{}, *actual* **{}x{}**)".format(
            self.title_resolution[0], self.title_resolution[1],
            self.image_resolution[0], self.image_resolution[1]
        )


RULES = [ResolutionAny, ResolutionBad, AspectRatioBad, ResolutionMismatch]
