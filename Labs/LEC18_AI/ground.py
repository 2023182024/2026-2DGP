from pico2d import load_image, get_canvas_width, get_canvas_height


class Ground:
    def __init__(self):
        self.image = load_image('TUK_GROUND.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(get_canvas_width() // 2, get_canvas_height() // 2)
