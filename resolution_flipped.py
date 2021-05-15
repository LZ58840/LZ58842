from resolution_any import ResolutionAny


class ResolutionFlipped(ResolutionAny):
    def __init__(self, post):
        super().__init__(post)
        super().evaluate()
        self.type = post.link_flair_text
        self.grab_resolution()