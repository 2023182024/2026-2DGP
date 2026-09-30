from pico2d import *

open_canvas()

qiqi= load_image('qiqi_sprite(made_by_gemini)_transparent.png')
grass= load_image('grass.png')

canvas_width=800
canvas_height=600

def draw_update(grass):
    grass.draw(400,135)
    update_canvas()
    delay(0.5)

while True:
    
    print("walking")
    x=522
    for index in range(20,376,86):
        clear_canvas()
        qiqi.clip_draw(
            index,x,
            52,86,
            400,300,
            canvas_width/2,canvas_height/2
        )
        draw_update(grass)

    print("running")
    x=402
    for index in range(15,723, 85):
        clear_canvas()
        qiqi.clip_draw(
            index,x,
            70,88,
            400,300,
            canvas_width/2,canvas_height/2
        )
        draw_update(grass)

    print("jumping")
    x=10
    for index in range(20,503,120):
        clear_canvas()
        qiqi.clip_draw(
            index,x,
            50,130,
            400,310,
            canvas_width/2,canvas_height/2
        )
        draw_update(grass)
    
    print("attacking")
    x=402
    for index in range(723,1339, 85):
        clear_canvas()
        qiqi.clip_draw(
            index,x,
            70,87,
            400,300,
            canvas_width/2,canvas_height/2
        )
        draw_update(grass)
    
    print("skill")
    x=147
    for index in range(20,1092,118):
        clear_canvas()
        qiqi.clip_draw(
            index,x,
            90,92,
            400,300,
            canvas_width/2,canvas_height/2
        )
        draw_update(grass)
    pass