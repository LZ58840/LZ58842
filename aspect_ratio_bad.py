from resolution_bad import ResolutionBad
from search_exp import ASPECT_RATIO


class AspectRatioBad(ResolutionBad):
    def __init__(self, post):
        super().__init__(post)
        self.aspect_ratio = round(self.width / self.height, 3)

    def evaluate(self):
        if self.type == "Mobile":
            return self.aspect_ratio <= ASPECT_RATIO["Mobile"]
        elif self.type == "Desktop":
            return self.aspect_ratio >= ASPECT_RATIO["Desktop"]

    def to_string(self):
        req = ""
        if self.type == "Mobile":
            req += " (W/H {0} or less)**\n\nyour aspect ratio (W/H): **{1}** (> {0}, too wide)".format(
                ASPECT_RATIO["Mobile"],
                self.aspect_ratio
            )
        elif self.type == "Desktop":
            req += " (W/H {0} or more)**\n\nyour aspect ratio (W/H): **{1}** (< {0}, too tall)".format(
                ASPECT_RATIO["Desktop"],
                self.aspect_ratio
            )
        return 2, "**aspect ratio** of {} wallpaper **must be proper".format(self.post.link_flair_text.lower()) + req


