from pico2d import *
open_canvas(800, 600)

x = 300
y = 200

character = load_image('character.png')

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
        delay(0.05)
    x=300
    y=200
    pass

def move_rectangle(x,y):
    while x < 800:
        clear_canvas()
        x+=5
        print(x, y)
        character.draw(x, y)
        delay(0.01)
    while y < 600:
        clear_canvas()
        y+=5
        print(x, y) 
        character.draw(x, y)
        delay(0.01)
    while x > 0:
        clear_canvas()
        x-=5
        print(x, y)
        character.draw(x, y)
        delay(0.01)
    while y > 0:
        clear_canvas()
        y-=5
        print(x, y)
        character.draw(x, y)
        delay(0.01)
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