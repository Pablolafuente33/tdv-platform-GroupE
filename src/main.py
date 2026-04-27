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
ROOM_W      = ROOM_RIGHT  - ROOM_LEFT
ROOM_H      = ROOM_TOP    - ROOM_BOTTOM

#Colores de la habitación
COLOR_WALL  = (60, 60, 60)   


# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
PLAYER_RADIUS = 20
DOOR_TILES = 3


# CONSTANTES DE LA INFO DEL PPROTAGONISTA
HUD_MARGIN      = (WINDOW_WIDTH // 2) - 161         # Margen desde los bordes de pantalla
HUD_BAR_W       = 260         # Anchura de la barra de vida
HUD_BAR_H       = 20          # Altura de la barra de vida
HUD_SLOT_SIZE   = 58          # Tamaño de cada slot de inventario
HUD_SLOT_GAP    = 8           # Separación entre slots
HUD_SLOT_Y      = 16  # Distancia desde el borde inferior
 
# Paleta medieval
C_DARK      = (26,  18,   8)
C_GOLD      = (212, 160,  48)
C_GOLD_DIM  = (107,  74,  26)
C_HP_HIGH   = (200,  40,  40)
C_HP_MED    = (200, 120,   0)
C_HP_LOW    = (140,  16,  16)
C_SLOT_BG   = (30,  20,  10)
C_SLOT_EQ   = (42,  30,  12)
C_WHITE     = (255, 255, 255)
C_MUTED     = (160, 128,  64)


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

        #Las teclas que estan siendo presionadas
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        #Iniciamos las variables de nuestros sprites.
        self.player_sprite = None
        self.wall_list = None
        self.scene = None

        # Motor de física
        self.physics_engine = None

        #Entorno
        self.door_rects      = []
        self.current_room_id = 0

        #cámaras
        self.camera = None
        self.gui_camera = None
        
        #Sonidos
        self.gameover_sound = arcade.load_sound(":resources:sounds/gameover1.wav")

    def setup(self):
        self.background_color = arcade.color.BLACK

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
       
        item = self.player_sprite.objeto_equipado()
        
        """
        arcade.draw_text(
            f"Equipado: {item}" if item else "Sin objeto",
            10, 40, arcade.color.YELLOW, 16 )
       
        arcade.draw_text(
            "WASD / Flechas · ESC = menú",
            10, 10, arcade.color.WHITE, 13
        )
        """
        self.draw_info()

    def draw_info(self):
        """Dibuja la barra de vida y el inventario en la esquina inferior izquierda."""
        player = self.player_sprite
 
        # ── Posición base del HUD ────────────────────────────────────────
        hud_x = HUD_MARGIN
        # Los slots van en la parte inferior
        slots_y   = HUD_SLOT_Y
        slots_top = slots_y + HUD_SLOT_SIZE
 
        # La barra de vida va justo encima de los slots
        bar_y   = slots_top + 20
        bar_top = bar_y + HUD_BAR_H
 
        # ── Barra de vida ────────────────────────────────────────────────
        hp_pct = player.health / player.max_health
 
        # Fondo de la barra
        arcade.draw_lrbt_rectangle_filled(
            hud_x, hud_x + HUD_BAR_W,
            bar_y, bar_top,
            (20, 12, 4)
        )
        # Borde dorado
        arcade.draw_lrbt_rectangle_outline(
            hud_x, hud_x + HUD_BAR_W,
            bar_y, bar_top,
            C_GOLD_DIM, 2
        )
 
        # Relleno de vida con color dinámico
        if hp_pct > 0.5:
            hp_color = C_HP_HIGH
        elif hp_pct > 0.25:
            hp_color = C_HP_MED
        else:
            hp_color = C_HP_LOW
 
        fill_w = int(HUD_BAR_W * hp_pct)
        if fill_w > 0:
            arcade.draw_lrbt_rectangle_filled(
                hud_x, hud_x + fill_w,
                bar_y, bar_top,
                hp_color
            )
            # Reflejo interior
            arcade.draw_lrbt_rectangle_filled(
                hud_x + 2, hud_x + fill_w - 2,
                bar_top - 6, bar_top - 2,
                (255, 200, 200, 60)
            )
 
        # Texto de vida
        arcade.draw_text(
            f"{player.health} / {player.max_health}",
            hud_x + HUD_BAR_W - 4, bar_y + HUD_BAR_H // 2,
            C_GOLD, font_size=11, anchor_x="right", anchor_y="center",
            bold=True
        )
 
        # Etiqueta "VIDA"
        arcade.draw_text(
            "\u2665 VIDA",
            hud_x, bar_top + 4,
            C_MUTED, font_size=10, bold=True
        )
 
        # ── Inventario ───────────────────────────────────────────────────
        for i in range(5):
            sx = hud_x + i * (HUD_SLOT_SIZE + HUD_SLOT_GAP)
            sy = slots_y
            cx = sx + HUD_SLOT_SIZE // 2
            cy = sy + HUD_SLOT_SIZE // 2
            #Cogemos el item del inventario
            if i < len(player.inventario):
                item = player.inventario[i]
            else:  
                item = None

            is_eq = (item != None) and (i == player.equipped_index)
            empty = item == None
    
            # Fondo del slot
            arcade.draw_lrbt_rectangle_filled(
                sx, sx + HUD_SLOT_SIZE,
                sy, sy + HUD_SLOT_SIZE,
                C_SLOT_EQ if is_eq else C_SLOT_BG
            )
 
            # Borde: dorado si equipado, oscuro si no
            border_color = C_GOLD if is_eq else C_GOLD_DIM
            border_w     = 2     if is_eq else 1
            arcade.draw_lrbt_rectangle_outline(
                sx, sx + HUD_SLOT_SIZE,
                sy, sy + HUD_SLOT_SIZE,
                border_color, border_w
            )
 
            # Esquineras decorativas (solo en slots con item)
            if not empty:
                d = 6
                corners = [
                    (sx,                       sy + HUD_SLOT_SIZE - d, d, 1),
                    (sx,                       sy + HUD_SLOT_SIZE - d, 1, d),
                    (sx + HUD_SLOT_SIZE - d,   sy + HUD_SLOT_SIZE - d, d, 1),
                    (sx + HUD_SLOT_SIZE - 1,   sy + HUD_SLOT_SIZE - d, 1, d),
                    (sx,                       sy,                     d, 1),
                    (sx,                       sy,                     1, d),
                    (sx + HUD_SLOT_SIZE - d,   sy,                     d, 1),
                    (sx + HUD_SLOT_SIZE - 1,   sy,                     1, d),
                ]
                for (ex, ey, ew, eh) in corners:
                    arcade.draw_lrbt_rectangle_filled(ex, ex+ew, ey, ey+eh, C_GOLD)
 
            if empty:
                # Slot vacío: cruz tenue en el centro
                arcade.draw_text(
                    "+", cx, cy,
                    (50, 38, 20), font_size=22,
                    anchor_x="center", anchor_y="center"
                )
            else:
                # Icono del objeto
                padding = 8
                arcade.draw_texture_rect(
                    item.texture, #La dirección que le pasamos antes se ha pasado a una textura
                    arcade.LRBT(
                        sx + padding,
                        sx + HUD_SLOT_SIZE - padding,
                        sy + padding + 8,
                        sy + HUD_SLOT_SIZE - padding
                    )
                )
                # Nombre
                arcade.draw_text(
                    item.nombre,
                    cx, sy + 5,
                    C_GOLD if is_eq else C_MUTED,
                    font_size=8, anchor_x="center", bold=is_eq
                )
 
            # Etiqueta "EQUIPADO" encima del slot activo
            if is_eq:
                arcade.draw_lrbt_rectangle_filled(
                    cx - 22, cx + 22,
                    sy + HUD_SLOT_SIZE + 1, sy + HUD_SLOT_SIZE + 12,
                    C_GOLD
                )
                arcade.draw_text(
                    "EQUIPADO",
                    cx, sy + HUD_SLOT_SIZE + 2,
                    C_DARK, font_size=7, anchor_x="center", bold=True
                )
 

    def on_update(self, delta_time):
        #Movemos al ppersonaje usando las físicas del juego
        self.physics_engine.update()

        # Actualizamos la animación del personaje
        self.player_sprite.update_animation(delta_time)

    """
    ============================================================================================================
    =====================================  INPUT DEL USUARIO  ==================================================
    ============================================================================================================
    """
    def on_key_press(self, key, modifiers):
        #Si pulsamos la tecla de escape vamos al menú de configuración.
        if key == arcade.key.ESCAPE:
            menu_view = MainMenu()
            self.window.show_view(menu_view)
            return
        
        #Teclas para mover el personaje
        if key in [arcade.key.LEFT, arcade.key.A]:
            self.left_pressed = True
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.right_pressed = True
        elif key in [arcade.key.UP, arcade.key.W]:
            self.up_pressed  = True
        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.down_pressed = True
        
        # Botón para usar el arma
        elif key == arcade.key.SPACE:
            self.player_sprite.usar_objeto()
        
        #Testeo de la barra de vida
        elif key == arcade.key.F:
            self.player_sprite.health -= 25
            
        #Calculamos la nueva posición
        self.actualizar_jugador()
    
    def on_key_release(self, key, modifiers):
        if key in [arcade.key.LEFT, arcade.key.A]:
            self.left_pressed = False
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.right_pressed = False
        elif key in [arcade.key.UP, arcade.key.W]:
            self.up_pressed  = False
        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.down_pressed = False

        #Hacemos el cálculo para que la pausa esté bien
        self.actualizar_jugador()
    #Mecánica del scroll de ratón
    def on_mouse_scroll(self, scroll_y):
        if scroll_y > 0:
            self.player_sprite.objeto_siguiente()
        elif scroll_y < 0:
            self.player_sprite.objeto_anterior()

    """
    ============================================================================================================
    ==================================== MOVIMIENTO DEL PERSONAJE  =============================================
    ============================================================================================================
    """
    def actualizar_jugador(self):
        #Determinamos la dirección
        dir_x = 0
        dir_y = 0

        if self.up_pressed: dir_y += 1
        if self.down_pressed: dir_y -= 1
        if self.left_pressed: dir_x -= 1 
        if self.right_pressed: dir_x += 1

        #Si nos movemos en diagonal
        if dir_x != 0 and dir_y != 0:
            #Calculamos el tamaño del vector
            tam = math.sqrt(dir_x**2 + dir_y**2)
            #posición normalizada
            self.player_sprite.change_x = (dir_x/tam) * PLAYER_MOVEMENT_SPEED
            self.player_sprite.change_y = (dir_y/tam) * PLAYER_MOVEMENT_SPEED
        else:
            #Movimiento normal / en una sola dirección
            self.player_sprite.change_x = dir_x * PLAYER_MOVEMENT_SPEED
            self.player_sprite.change_y = dir_y * PLAYER_MOVEMENT_SPEED

    #Mecánicas de disparos 
    def testear_arma(self):
        """
        Aquí es donde TÚ programarás tus armas.
        Ejemplo de detección de colisión simple:
        """
        if arcade.check_for_collision(self.jugador, self.enemigo):
            print("¡Impacto detectado!")
            self.enemigo.vida -= 10
            if self.enemigo.vida <= 0:
                self.enemigo.remove_from_sprite_lists()

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).parent.parent
    print(f"Project root is: {PROJECT_ROOT}")
    main()