from pico2d import *
import math
open_canvas(800, 600)

x = 300
y = 200

character = load_image('character.png')

def draw_character(x, y):
    clear_canvas()
    character.draw(x,y)
    update_canvas()
    print(x, y)
    delay(0.05)

def draw_up(x,y):

    pass

def draw_rignt(x,y):

    pass

def draw_down(x,y):

    pass

def draw_left(x,y):

    pass

def move_circle(x,y):
    print('CIRCLE')
    for deg in range(0,360,5):
        rad=math.radians(deg)
        x=400+200*math.cos(rad)
        y=300+200*math.sin(rad)
        draw_character(x, y)
    pass


def move_rectangle(x,y):
    print('RECTANGLE')
    draw_up(x,y)
    draw_rignt(x,y)
    draw_down(x,y)
    draw_left(x,y)
    pass


def move_triangle(x,y):
    while x < 500:
        clear_canvas()
        x+=4
        print(x, y)
        character.draw(x, y)
        update_canvas()
        delay(0.01)
    while y < 400:
        clear_canvas()
        y+=4
        x-=2
        print(x, y)
        character.draw(x, y)
        update_canvas()
        delay(0.01)
    while x > 300:
        clear_canvas()
        x-=2
        y-=4
        print(x, y)
        character.draw(x, y)
        update_canvas()
        delay(0.01)
    clear_canvas()


    character.draw(x, y)
    pass



while True:
    move_circle(x, y)
    move_rectangle(x, y)
    move_triangle(x, y)
    pass
    
close_canvas() 