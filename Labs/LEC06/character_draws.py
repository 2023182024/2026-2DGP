from pico2d import *
open_canvas(800, 600)

x = 300
y = 200

character = load_image('character.png')

def move_circle(x,y):
    clear_canvas()

    pass

def move_rectangle(x,y):
    clear_canvas()
    if x < 500 and y==200:
        x += 2
    elif x==500 and y < 400:
        y += 2
    elif x > 300 and y==400:
        x -= 2
    elif x==300 and y > 200:
        y -= 2
    character.draw(x, y)
    pass

def move_triangle(x,y):
    clear_canvas()
    pass



while True:
    move_circle(x, y)
    move_rectangle(x, y)
    move_triangle(x, y)
    pass
    
close_canvas() 