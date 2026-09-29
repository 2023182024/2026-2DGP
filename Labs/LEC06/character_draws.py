from pico2d import *
import math
open_canvas(800, 600)

x = 300
y = 200

character = load_image('character.png')

def draw_line(a,b):
    start=a
    end=a+200
    for a in range(start,end,4):
        character.draw(a,b)
        update_canvas()
        delay(0.05)
    pass

def draw_decline(a,b):
    start=a
    end=a-200
    for a in range(start,end,-4):
        character.draw(a,b)
        update_canvas()
        delay(0.05)
    pass

def move_circle(x,y):
    radius = 200
    angle = 0
    while angle < 2 * 3.14:
        clear_canvas()
        x = 400 + radius * math.cos(angle)
        y = 300 + radius * math.sin(angle)
        character.draw(x, y)
        angle += 0.1
        print(x,y,angle)
        update_canvas()
        delay(0.05)
    x=300
    y=200
    pass

def move_rectangle(x,y):
    x=300
    y=200
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