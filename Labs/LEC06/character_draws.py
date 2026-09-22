from pico2d import *
open_canvas(800, 600)

x = 300
y = 200

character = load_image('character.png')

def move_circle(x,y):
    clear_canvas()

    pass

def move_rectangle(x,y):
    while x < 800:
        clear_canvas()
        x+=2
        print(x, y)
        character.draw(x, y)
    while y < 600:
        clear_canvas()
        y+=2
        print(x, y) 
        character.draw(x, y)
    while x > 0:
        clear_canvas()
        x-=2
        print(x, y)
        character.draw(x, y)
    while y > 0:
        clear_canvas()
        y-=2
        print(x, y)
        character.draw(x, y)
    pass

def move_triangle(x,y):
    clear_canvas()


    character.draw(x, y)
    pass



while True:
    move_circle(x, y)
    move_rectangle(x, y)
    move_triangle(x, y)
    pass
    
close_canvas() 