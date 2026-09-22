from pico2d import *

open_canvas(800,600)
character = load_image('character.png')

x=0
y=0

while True:

    while x<800:
        clear_canvas()
        character.draw(x,y)
        update_canvas()
        x += 5
        delay(0.01)

    while y<600:
        clear_canvas()
        character.draw(x,y)
        update_canvas()
        y += 5
        delay(0.01)

    while x>0:
        clear_canvas()
        character.draw(x,y)
        update_canvas()
        x -= 5
        delay(0.01)

    while y>0:
        clear_canvas()
        character.draw(x,y)
        update_canvas()
        y -= 5
        delay(0.01)



