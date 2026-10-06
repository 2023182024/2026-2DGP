"""키보드로 Sonic 스프라이트 애니메이션을 확인하는 뷰어."""

from pathlib import Path

try:
    from pico2d import *
except ImportError as error:
    raise SystemExit("Pico2D 라이브러리를 설치한 Python 환경에서 실행하세요.") from error


def main():
    canvas_open = False
    try:
        open_canvas()
        canvas_open = True
    finally:
        if canvas_open:
            close_canvas()


if __name__ == "__main__":
    main()
