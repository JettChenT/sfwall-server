url = "https://source.unsplash.com"


class Unsplash:
    def __init__(self):
        pass

    def get_random_img(self, resolution="5120x3200"):
        return f"{url}/random/{resolution}"
