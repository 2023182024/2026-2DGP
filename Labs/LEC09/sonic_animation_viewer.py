"""키보드로 Sonic 스프라이트 애니메이션을 확인하는 뷰어."""

from pathlib import Path

try:
    from pico2d import *
except ImportError as error:
    raise SystemExit("Pico2D 라이브러리를 설치한 Python 환경에서 실행하세요.") from error

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 600
TARGET_FPS = 60

running = True


def handle_events():
    """창 닫기와 Esc 종료 입력을 처리한다."""
    global running

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def main():
    global running
    canvas_open = False
    try:
        open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
        canvas_open = True
        running = True
        while running:
            handle_events()
            clear_canvas()
            update_canvas()
            delay(1.0 / TARGET_FPS)
    finally:
        if canvas_open:
            close_canvas()


if __name__ == "__main__":
    main()
