"""
Platformer Game. 

Basado en el tutorial de arcade: https://arcade.academy/examples/platform_tutorial.html#platform-tutorial
"""
import math

from pathlib import Path

import arcade
from personajes import Protagonista

"""
----------------------------------------------------------------------------
-------------               CONSTANTES              ------------------------
----------------------------------------------------------------------------
"""

# ConstaNTES DE VENTANA
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "MEDIAVAL FIGTH"

#Constyantes para cada habitación
TILE_SIZE = 64
WALL_COLS       = WINDOW_WIDTH  // TILE_SIZE  # 20 columnas
WALL_ROWS       = WINDOW_HEIGHT // TILE_SIZE  # 11 filas

# Área jugable (interior de las paredes)
ROOM_LEFT   = TILE_SIZE
ROOM_RIGHT  = WINDOW_WIDTH  - TILE_SIZE
ROOM_BOTTOM = TILE_SIZE
ROOM_TOP    = WINDOW_HEIGHT - TILE_SIZE

#Colores de la habitación
COLOR_WALL  = (60, 60, 60)   


# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
PLAYER_RADIUS = 20

"""
----------------------------------------------------------------------------
---------               MENÚ DE CONFIGURACIÓN           --------------------
----------------------------------------------------------------------------
"""

class MainMenu(arcade.View):
    def on_show_view(self):
        self.window.background_color = arcade.color.WHITE

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Main Menu - Click To Play",
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center"
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

"""
-------------------------------------------------------------------------------------
-----------             VISTA   GENERAL     DEL     JUEGO           -----------------
-------------------------------------------------------------------------------------
"""
class GameView(arcade.View):
    """
    Main application class.
    """
    def __init__(self, window = None, background_color = None):
        super().__init__(window, background_color)

        #Estado de las teclas al inicio
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.shoot_pressed = False

        #Iniciamos las variables de nuestro personaje
        self.player_sprite = None
        self.wall_list = None
        self.scene = None

        # Motor de física
        self.physics_engine = None

        #cámaras
        self.camera = None
        self.gui_camera = None

    def setup(self):
        self.background_color = arcade.color.DARK_BROWN

        #Iniciamos las paredes 
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.build_room()
        #iniciamos el sprite de nuestro personaje
        self.player_sprite = Protagonista()
            #Lo inicializamos en e medio de la aplicación
        self.player_sprite.center_x = WINDOW_WIDTH //2  
        self.player_sprite.center_y = WINDOW_HEIGHT //2 

        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Walls", sprite_list=self.wall_list)
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self.player_sprite)

        #Inicializamos el motor de físicas
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.wall_list
        )

        #Inicializamos las cámaras
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()
    
    def build_room(self):
        """Rellena el borde de la pantalla con tiles de pared."""
        for col in range(WALL_COLS):
            for row in range(WALL_ROWS):
                is_wall = (col == 0 or col == WALL_COLS - 1 or
                           row == 0 or row == WALL_ROWS - 1)
                if is_wall:
                    wall = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE, (60,60,60))
                    wall.center_x = col * TILE_SIZE + TILE_SIZE // 2
                    wall.center_y = row * TILE_SIZE + TILE_SIZE // 2
                    self.wall_list.append(wall)

    def on_draw(self):
        self.clear() #Siempre al principio del on_draw

        #iniciamos la cámara antes de dibujar
        self.camera.use()

        #Suelo interior
        arcade.draw_lrbt_rectangle_filled(
            ROOM_LEFT, ROOM_RIGHT, ROOM_BOTTOM, ROOM_TOP,
            arcade.color.DARK_BROWN
        )

        #Dibujamos la escena que tiene las paredes y al personaje
        self.scene.draw()

        # HUD (cámara GUI fija)
        self.gui_camera.use()
       
        arcade.draw_text(
            "WASD / Flechas · ESC = menú",
            10, 10, arcade.color.WHITE, 13
        )

    def on_update(self, delta_time):
        #Movemos al ppersonaje usando las físicas del juego
        self.physics_engine.update()

        #Nuestra cámara siempre encima del personaje
        self.camera.position = self.player_sprite.position

        # Actualizamos la animación del personaje
        self.player_sprite.update_animation(delta_time)

    
    def on_key_press(self, key, modifiers):
        #Si pulsamos la tecla de escape vamos al menú de configuración.
        if key == arcade.key.ESCAPE:
            menu_view = MainMenu()
            self.window.show_view(menu_view)
            return
        """
        Esto se cambiará más adelante ya que será una vista diferente a la hora de pausar 
        que a la hora de que vayamos a abrirlo de principio

        """

        if key in [arcade.key.UP, arcade.key.W]:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.LEFT, arcade.key.A]:
            self.player_sprite.change_x = 0
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.player_sprite.change_x = 0
        elif key in [arcade.key.UP, arcade.key.W]:
            self.player_sprite.change_y  = 0
        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.player_sprite.change_y = 0



def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).parent.parent
    print(f"Project root is: {PROJECT_ROOT}")
    main()