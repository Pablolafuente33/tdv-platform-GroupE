"""
Platformer Game. 

Basado en el tutorial de arcade: https://arcade.academy/examples/platform_tutorial.html#platform-tutorial
"""
from pathlib import Path

import arcade

from constantes import *

from views.title import TitleView

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    
    menu_view = TitleView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).parent.parent
    print(f"Project root is: {PROJECT_ROOT}")
    main()