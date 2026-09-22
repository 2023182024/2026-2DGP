from pico2d import *

open_canvas(800, 600)
character = load_image('character.png')

x = 0
y = 0
direction = 'right'

while True:
    if direction == 'right':
        x += 5
        if x >= 800:
            x = 800
            direction = 'up'
    elif direction == 'up':
        y += 5
        if y >= 600:
            y = 600
            direction = 'left'
    elif direction == 'left':
        x -= 5
        if x <= 0:
            x = 0
            direction = 'down'
    elif direction == 'down':
        y -= 5
        if y <= 0:
            y = 0
            direction = 'right'

    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)