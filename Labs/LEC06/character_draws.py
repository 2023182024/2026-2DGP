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

def draw_line(a,b):

    pass

def draw_decline(a,b):

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
    draw_line(x,y)
    draw_line(y,x)
    draw_decline(x,y)
    draw_decline(y,x)
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