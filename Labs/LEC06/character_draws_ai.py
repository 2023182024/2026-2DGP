import math
from pico2d import *

open_canvas(800, 600)
character = load_image('character.png')

def move_circle():
    cx, cy, r = 400, 300, 200
    angle = 0
    while angle < 2 * math.pi:
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        clear_canvas()
        character.draw(x, y)
        update_canvas()
        angle += 0.05
        delay(0.01)

def move_rectangle():
    x, y = 200, 100
    while x < 600:
        clear_canvas()
        x += 5
        character.draw(x, y)
        update_canvas()
        delay(0.01)
    while y < 500:
        clear_canvas()
        y += 5
        character.draw(x, y)
        update_canvas()
        delay(0.01)
    while x > 200:
        clear_canvas()
        x -= 5
        character.draw(x, y)
        update_canvas()
        delay(0.01)
    while y > 100:
        clear_canvas()
        y -= 5
        character.draw(x, y)
        update_canvas()
        delay(0.01)

def move_triangle():
    steps = 100
    apexes = ((400, 500), (200, 150), (600, 100))
    for i in range(len(apexes)):
        ax, ay = apexes[i]
        bx, by = apexes[(i + 1) % len(apexes)]
        for step in range(steps):
            x = ax + (bx - ax) * step / steps
            y = ay + (by - ay) * step / steps
            clear_canvas()
            character.draw(x, y)
            update_canvas()
            delay(0.01)

while True:
    move_circle()
    move_rectangle()
    move_triangle()