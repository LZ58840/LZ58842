"""User defined characteristics of submissions to skip."""


def is_text_post(submission):
    return submission.selftext != ""


def is_other_wallpaper(submission):
    return submission.link_flair_text not in ["Desktop", "Mobile"]


SKIP_FLAGS = [is_text_post, is_other_wallpaper]
