import math
from pico2d import *

open_canvas(800, 600)
character = load_image('character.png')

center_x = 400
center_y = 300
radius = 200
angle = 0

while True:
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)

    clear_canvas()
    character.draw(x, y)
    update_canvas()

    angle += 0.05
    if angle >= math.pi * 2:
        angle -= math.pi * 2
    delay(0.01)