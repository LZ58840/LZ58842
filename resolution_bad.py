import logging
import requests
import shutil

from resolution_any import ResolutionAny
from search_exp import RESOLUTION_MIN
from PIL import Image


class ResolutionBad(ResolutionAny):
    def __init__(self, post):
        super().__init__(post)
        self.type = post.link_flair_text
        self.grab_resolution()

    def grab_resolution(self):
        get_img = requests.get(self.post.url, stream=True)
        if get_img.status_code == 200:
            get_img.raw.decode_content = True
            with open("img.dat", 'wb') as img:
                shutil.copyfileobj(get_img.raw, img)
            img.close()
            image = Image.open("img.dat")
            self.width, self.height = image.size
        else:
            logging.error("Image could not be retrieved.")

    def evaluate(self):
        return self.width >= RESOLUTION_MIN[self.type][0] and self.height >= RESOLUTION_MIN[self.type][1]

    def to_string(self):
        return 2, "**resolution** of {} wallpaper must be **minimum {}x{}**".format(
            self.post.link_flair_text.lower(),
            RESOLUTION_MIN[self.type][0],
            RESOLUTION_MIN[self.type][1]
        )
