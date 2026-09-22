from pico2d import *


open_canvas(800, 600)
character = load_image('character.png')

radius = 200

while True:


    while radius >0:
        clear_canvas()
        character.draw(200+radius,300+radius)
        update_canvas()
        radius-=2
        delay(0.01)

    while radius <200:
            clear_canvas()
            character.draw(200+radius,300-radius)
            update_canvas()
            radius+=2
            delay(0.01)
    
    while radius >0:
        clear_canvas()
        character.draw(600-radius,300-radius)
        update_canvas()
        radius-=2
        delay(0.01)

    while radius <200:
        clear_canvas()
        character.draw(600-radius,300+radius)
        update_canvas()
        radius+=2
        delay(0.01)