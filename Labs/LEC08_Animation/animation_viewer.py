from pico2d import *

open_canvas()

qiqi = load_image('qiqi_sprite(made_by_gemini)_transparent.png')

# Walking row, columns 1 through 5. Each tuple is (left, top, width, height)
# in image coordinates measured from the upper-left corner.
IMAGE_HEIGHT = 768
WALKING_FRAMES = [
    (20, 159, 45, 87),
    (106, 159, 42, 87),
    (193, 159, 42, 87),
    (280, 159, 42, 86),
    (376, 159, 42, 87),
]

while True:
    for source_x, top_y, frame_w, frame_h in WALKING_FRAMES:
        # clip_draw uses source coordinates measured from the bottom-left.
        source_y = IMAGE_HEIGHT - top_y - frame_h

        clear_canvas()
        qiqi.clip_draw(
            source_x, source_y,
            frame_w, frame_h,
            100, 100
        )
        update_canvas()
        delay(0.5)
