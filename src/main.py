"""
Platformer Game. 

Basado en el tutorial de arcade: https://arcade.academy/examples/platform_tutorial.html#platform-tutorial
"""
import math
import os

from pathlib import Path

import arcade
import arcade.gui
from Entidades.Player import Player
from Habitaciones import HABITACIONES, OPUESTO

#Para mantener el aspecto retro
from pyglet.gl import GL_NEAREST



"""
----------------------------------------------------------------------------
-------------               CONSTANTES              ------------------------
----------------------------------------------------------------------------
"""

# ConstaNTES DE VENTANA
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 704
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

"""
----------------------------------------------------------------------------
---------                INTERFAZ DE MENÚS (GUI)                ------------
----------------------------------------------------------------------------
"""

class TitleView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        
        # Cargamos las imágenes del fondo y los botones
        graficos = os.path.join('assets', 'graphics')
        self.background = arcade.load_texture(os.path.join(graficos, 'fondo_menu.png'))
        self.tex_jugar = arcade.load_texture(os.path.join(graficos,'boton_jugar.png'))
        self.tex_ajustes = arcade.load_texture(os.path.join(graficos,'boton_ajustes.png'))

        #Musica de inicio
        self.load_music = arcade.load_sound(os.path.join('assets','music','InitSound.mp3'), streaming= True)
        
    def on_show_view(self):
        self.manager.enable()
        self.setup_gui()
        self.musica_inicio = self.load_music.play(loop = True)  #-- #Lo comento porque con las pruebas me está poniendo nervioso

    def on_hide_view(self):
        self.musica_inicio.pause()

    def setup_gui(self):
        self.manager.clear()
        
        anchor = arcade.gui.UIAnchorLayout()
        
        self.v_box = arcade.gui.UIBoxLayout(space_between=5)

        # Creación del botón de JUGAR
        play_button = arcade.gui.UITextureButton(
            texture=self.tex_jugar,
            texture_hovered=self.tex_jugar,
            texture_pressed=self.tex_jugar,
            text="", 
            width=350,
            height=175
        )
        
        # Creación del botón de AJUSTES
        settings_button = arcade.gui.UITextureButton(
            texture=self.tex_ajustes,
            texture_hovered=self.tex_ajustes,
            texture_pressed=self.tex_ajustes,
            text="",
            width=350,
            height=175
        )

        self.v_box.add(play_button)
        self.v_box.add(settings_button)

        # Eventos al hacer click en los botones
        @play_button.event("on_click")
        def on_click_play(event):
            self.manager.disable()
            # arcade.stop_sound(self.musica_inicio)
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
            

        @settings_button.event("on_click")
        def on_click_settings(event):
            self.manager.disable()
            self.window.show_view(SettingsView())

        # Se establece la posición:
        anchor.add(
            child=self.v_box, 
            anchor_x="center", 
            anchor_y="center", 
            align_y=-80
        )
        
        self.manager.add(anchor)

    def on_draw(self):
        self.clear()
        
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.LRBT(
                left=0, 
                right=WINDOW_WIDTH, 
                bottom=0, 
                top=WINDOW_HEIGHT
            )
        )
        
        
        # Dibujamos los botones
        self.manager.draw()

class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        
        graficos = os.path.join('assets', 'graphics')
        
        # Fondo específico para ajustes
        self.background = arcade.load_texture(os.path.join(graficos, 'fondo_ajustes.png'))
        
        # Textura para el botón VOLUMEN
        self.tex_volumen = arcade.load_texture(os.path.join(graficos, 'boton_volumen.png'))

        # Textura para el botón PANTALLA COMPLETA
        self.tex_pantalla = arcade.load_texture(os.path.join(graficos, 'boton_pantalla_completa.png'))
        
        # Textura para el botón VOLVER
        self.tex_volver = arcade.load_texture(os.path.join(graficos, 'boton_volver.png'))


    def on_show_view(self):
        self.manager.enable()
        self.setup_gui()

    def setup_gui(self):
        self.manager.clear()
        
        anchor = arcade.gui.UIAnchorLayout()
        v_box = arcade.gui.UIBoxLayout(space_between=20)

        vol_label = arcade.gui.UITextureButton(texture=self.tex_volumen, width=260, height=65)

        self.volume_slider = arcade.gui.UISlider(value=50, width=300)


        fullscreen_btn = arcade.gui.UITextureButton(
            texture=self.tex_pantalla, 
            width=260, 
            height=65
        )

        back_btn = arcade.gui.UITextureButton(
            texture=self.tex_volver,
            width=200,
            height=80
        )

        # --- EVENTOS ---

        @self.volume_slider.event("on_change")
        def on_volume_change(event):
            # Lógica para el volumen (0.0 a 1.0)
            vol = self.volume_slider.value / 100
            # arcade.set_volume(vol)
            pass

        @fullscreen_btn.event("on_click")
        @fullscreen_btn.event("on_click")
        def on_click_fullscreen(event):
            # Alternar el estado
            self.window.set_fullscreen(not self.window.fullscreen)
            
            # --- ESTO ES LO QUE FALTA ---
            # Obtenemos el nuevo tamaño físico de la ventana tras el cambio
            width, height = self.window.get_size()
            
            # Forzamos a Arcade a que proyecte nuestras coordenadas lógicas 
            # (1280x704) sobre el nuevo tamaño físico del monitor.
            self.window.set_viewport(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)

        @back_btn.event("on_click")
        def on_click_back(event):
            self.manager.disable()
            self.window.show_view(TitleView())

        # --- AGREGAR AL CONTENEDOR ---
        v_box.add(vol_label)
        v_box.add(self.volume_slider)
        v_box.add(fullscreen_btn)  # Ahora es el botón principal
        v_box.add(back_btn)

        anchor.add(child=v_box, anchor_x="center", anchor_y="center")
        self.manager.add(anchor)

    def on_draw(self):
        self.clear()
        
        # Dibujar fondo de ajustes
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.LRBT(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        )
        
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()


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
        self.enemy_list = None
        self.wall_list = None
        self.scene = None

        # Motor de física
        self.physics_engine = None

        #Entorno
        self.door_rects      = []
        self.current_room_id = 0
        self.puertas_bloqueadas = False

        #cámaras
        self.camera = None
        self.gui_camera = None
        self.pos_camara_x = WINDOW_WIDTH / 2
        self.pos_camara_y = WINDOW_HEIGHT/ 2
        self.cam_target_x    = WINDOW_WIDTH  / 2 
        self.cam_target_y    = WINDOW_HEIGHT / 2

        self.movimiento_camara = False
        
        #Sonidos
        self.gameover_sound = arcade.load_sound(":resources:sounds/gameover1.wav")

    """
    ===================================================================================================================
    ===============================================     SETUP     =====================================================
    ===================================================================================================================
    """
    def setup(self, room_id: int = 0, enter_from: str = None):
        #Para la inicialización veremos en que sala está y de que sala viene
        self.current_room_id = room_id
        self.background_color= arcade.color.BLACK
        self.door_rects = []
        room = HABITACIONES[room_id]

        #Cargamos el tilemap y obtenemos la escena
        self.scene = room.construir_habitacion()
        self.wall_list = room.get_wall_list()

        #Creamos las puertas para la detección de estas
        self.puertas_bloqueadas = arcade.SpriteList()
        for door in room.puertas:
            rect = self.__door_rect(door.side)
            self.door_rects.append((rect, door.side, door.leads_to))

            # Creamos una especie de "muro" para que no traspase mientras está cerrado
            rx,ry,rw,rh = rect
            muro_puerta = arcade.SpriteSolidColor(int(rw), int(rh),(0,0,0,0))
            muro_puerta.center_x = rx + rw / 2
            muro_puerta.center_y = ry + rh / 2
            self.puertas_bloqueadas.append(muro_puerta)

        ### INICialización del jugador

        if self.player_sprite is None:
            #iniciamos el sprite de nuestro personaje
            self.player_sprite = Player()
        
        #Será inicializado en la puerta de la sala en la que entra.
        self.player_sprite.change_y = 0
        self.player_sprite.change_x = 0
        sx, sy = self.__spawn_pos(enter_from)        
        self.player_sprite.center_x = sx
        self.player_sprite.center_y = sy

        self.scene.add_sprite("Player", self.player_sprite)

        # Motor del jugador 
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, [self.wall_list, self.puertas_bloqueadas]
        )

        # Enemigos, se crean en cada sala                         
        self.enemy_list = arcade.SpriteList()                              
        if not room.nivel_pasado:
            for enemigo in room.spawn():
                self.enemy_list.append(enemigo)

        self.scene.add_sprite_list("Enemigos", sprite_list = self.enemy_list)

        # Creamos una lista para los motores de los enemigos
        self.enemy_physics_engines = []
        for enemigo in self.enemy_list:
            # Cada enemigo tiene su motor contra muros y puertas
            engine = arcade.PhysicsEngineSimple(
                enemigo, [self.wall_list, self.puertas_bloqueadas]
            )
            self.enemy_physics_engines.append(engine)

        #Cámaras
        if self.camera is None:
            #Solo se crearán una vez
            self.camera = arcade.Camera2D()
            self.gui_camera = arcade.Camera2D()
        
        self.cam_target_x = WINDOW_WIDTH / 2
        self.cam_target_y = WINDOW_HEIGHT / 2

        #Si venimos de otra sala habrá transición en la cámara
        if enter_from is not None:
            self.movimiento_camara = True
        else:
            #En el caso de la primera sala
            self.pos_camara_x = self.cam_target_x
            self.pos_camara_y = self.cam_target_y
            self.movimiento_camara = False
        
        #Bloquearemos al jugador mientras la cámara se está moviento
        self.player_locked = enter_from is not None

    def __door_rect(self,side): #Definimos la función como privada ya que solo se va a utilizar aquí
        margin = 12
        tilemap = HABITACIONES[self.current_room_id].tile_map
        map_width = tilemap.width * tilemap.tile_width * tilemap.scaling
        map_height = tilemap.height * tilemap.tile_height * tilemap.scaling
        
        mid_x = map_width // 2
        mid_y = map_height // 2

        if side == 'r':
            cx, cy = map_width, mid_y
            w, h = margin + TILE_SIZE, DOOR_TILES * TILE_SIZE
        if side == 'l':
            cx, cy = 0, mid_y
            w, h = margin + TILE_SIZE, DOOR_TILES * TILE_SIZE
        if side == 'u':
            cx, cy = mid_x, map_height
            w, h = DOOR_TILES * TILE_SIZE, margin + TILE_SIZE
        if side == 'd':
            cx, cy = mid_x, 0
            w, h = DOOR_TILES * TILE_SIZE, margin + TILE_SIZE

        return (cx - w // 2, cy - h //2, w, h)
    
    #PAra el spawn del personaje
    def __spawn_pos(self, enter_form):
        tilemap = HABITACIONES[self.current_room_id].tile_map
        map_width = tilemap.width * tilemap.tile_width * tilemap.scaling
        map_height = tilemap.height * tilemap.tile_height * tilemap.scaling
        
        cx = map_width //2
        cy = map_height // 2

        margin = TILE_SIZE + 40
        if enter_form == 'r': return map_width - margin - TILE_SIZE, cy
        if enter_form == 'l': return  TILE_SIZE + margin, cy
        if enter_form == 'u': return cx, map_height- TILE_SIZE - margin
        if enter_form == 'd': return cx, TILE_SIZE + margin
        return cx, cy
    
    def __check_doors(self):
        #Solo si la cámara no está en transición
        if self.movimiento_camara:
            return
        
        # Bloqueo de puertas si hay enemigos vivos                         
        if len(self.enemy_list) > 0:                                       
            return    
        
        px = self.player_sprite.center_x
        py = self.player_sprite.center_y
    
        for(rx, ry, rw, rh), side, leads_to in self.door_rects:
            if rx <= px <= rx + rw and ry <= py <= ry + rh:
                self.setup(room_id=leads_to, enter_from = OPUESTO[side])
                return
            
    def __update_camera(self, delta_time):
        #Desliz suavemente hacia el objetivo
        self.pos_camara_x += (self.cam_target_x - self.pos_camara_x) * min(1.0, 4.0 * delta_time)
        self.pos_camara_y += (self.cam_target_y - self.pos_camara_y) * min(1.0, 4.0 * delta_time)

        self.camera.position = arcade.Vec2(self.pos_camara_x, self.pos_camara_y)

        #Comprobamos que la cámara está donde debería
        dist = abs(self.pos_camara_x - self.cam_target_x) + abs(self.pos_camara_y - self.cam_target_y)

        if dist < 1 :
            self.pos_camara_x = self.cam_target_x 
            self.pos_camara_y = self.cam_target_y
            self.movimiento_camara = False
            self.player_locked = False 
    
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

        #Puertas: Habrá un color diferente si están bloqueadas
        puertas_bloqueadas = len(self.enemy_list) > 0
        for door in HABITACIONES[self.current_room_id].puertas:
            self._draw_door_highlight(door.side, puertas_bloqueadas)
        
        #Dibujamos la escena que tiene las paredes y al personaje. Para evitar que los sprites se vean borrosos establecemos el filtro en NEAREST
        self.scene.draw(filter=GL_NEAREST)

        #Barras de vida de los enemigos
        for enemigo in self.enemy_list:
            self.__draw_enemy_hp(enemigo)
        
        # HUD (cámara GUI fija)
        self.gui_camera.use()
        
        self.draw_info()

        # Aviso de puertas bloqueadas                                      
        if puertas_bloqueadas:                                             
            arcade.draw_text(                                              
                f"¡Derrota a los enemigos! ({len(self.enemy_list)} restantes)",  
                WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40,                    
                (180,30,30), font_size=16,                                 
                anchor_x="center", bold=True                               
            )  

    
    """"
    --------------------------------------------------------------------------------------
    ------------------- Para dibujar el inventario y la barra de vida  -------------------
    --------------------------------------------------------------------------------------
    """
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
 
    def _draw_door_highlight(self, side, bloqueada=False):
        half = DOOR_TILES // 2

        tilemap = HABITACIONES[self.current_room_id].tile_map
        map_width = tilemap.width * tilemap.tile_width * tilemap.scaling
        map_height = tilemap.height * tilemap.tile_height * tilemap.scaling
        
        mid_x = map_width // 2
        mid_y = map_height // 2

        if side == 'r':
            x, y = map_width - TILE_SIZE, mid_y - (half + 0.5) * TILE_SIZE
            w, h = TILE_SIZE, DOOR_TILES * TILE_SIZE
        elif side == 'l':
            x, y = 0, mid_y - (half + 0.5) * TILE_SIZE
            w, h = TILE_SIZE, DOOR_TILES * TILE_SIZE
        elif side == 'u':
            x, y = mid_x - half * TILE_SIZE, map_height - TILE_SIZE
            w, h = DOOR_TILES * TILE_SIZE, TILE_SIZE
        elif side == 'd':
            x, y = mid_x - half * TILE_SIZE, 0
            w, h = DOOR_TILES * TILE_SIZE, TILE_SIZE

        # Rojo si bloqueada, dorado si abierta                            
        color_relleno  = (140, 20, 20) if bloqueada else (180, 140, 40)   
        color_borde    = (200, 40, 40) if bloqueada else C_GOLD            
        arcade.draw_lrbt_rectangle_filled(x, x+w, y, y+h, color_relleno + (180,))
        arcade.draw_lrbt_rectangle_outline(x, x+w, y, y+h, color_borde, 2)


    def __draw_enemy_hp(self, enemigo):                                   
        """Barra de vida pequeña encima de cada enemigo."""               
        bar_w = 40                                                        
        bar_h = 5                                                         
        x = enemigo.center_x - bar_w // 2                                 
        y = enemigo.center_y + enemigo.height // 2 + 6                    
        pct = max(0.0, enemigo.health / 100)                              
        arcade.draw_lrbt_rectangle_filled(x, x+bar_w, y, y+bar_h, (30, 10, 10))   
        arcade.draw_lrbt_rectangle_filled(x, x+int(bar_w*pct), y, y+bar_h, (180,30,30))  
        arcade.draw_lrbt_rectangle_outline(x, x+bar_w, y, y+bar_h, C_GOLD_DIM, 1) 
    """
    =======================================================================================================================================
    =================================================           ON UPDATE               ===================================================
    =======================================================================================================================================
    """
    def on_update(self, delta_time):
        #Si no se está haciendo la transición, el personaje se mueve al azar
        if not self.player_locked:
            self.player_sprite.actualizar_movimiento(self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed)
            self.physics_engine.update()
            self.__check_doors()

            #Si no hay enemigos es qeu nos hemos pasado el nivel.
            if len(self.enemy_list) == 0:
                self.puertas_bloqueadas.clear() #Limpiamos la lista donde están las puerrtas bloqueadas
                HABITACIONES[self.current_room_id].nivel_pasado = True

            # Actualizamos los motores de los enemigos (reemplaza tu bucle de enemigos por este)
            for i, enemigo in enumerate(self.enemy_list):
                # 1. IA: Decidir hacia dónde ir (esto solo cambia el change_x/y)
                distancia = math.sqrt((self.player_sprite.center_x - enemigo.center_x)**2 + 
                                    (self.player_sprite.center_y - enemigo.center_y)**2)
                
                if distancia < enemigo.detect_distance:
                    enemigo.seguir_jugador(self.player_sprite)
                else:
                    enemigo.caminar_aleatorio(delta_time)
                
                # 2. FÍSICAS: El motor mueve al enemigo y detecta muros
                # Solo actualizamos el motor si el enemigo sigue en la lista (vivo)
                if i < len(self.enemy_physics_engines):
                    self.enemy_physics_engines[i].update()
                
                # 3. Animación
                enemigo.update_animation(delta_time)
        
        #LLamamos para actualizar la cámara
        self.__update_camera(delta_time)
        
        # Actualizamos la animación del personaje
        self.player_sprite.update_animation_state(delta_time)
    """
    ============================================================================================================
    =====================================  INPUT DEL USUARIO  ==================================================
    ============================================================================================================
    """
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            # Volver a la pantalla de título
            title_view = TitleView()
            self.window.show_view(title_view)
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
        elif key == arcade.key.E:
            for enemy in self.enemy_list:
                enemy.recibir_danno(25)
            
        #Calculamos la nueva posición
        self.player_sprite.actualizar_movimiento(self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed)
    
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
        self.player_sprite.actualizar_movimiento(self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed)
    #Mecánica del scroll de ratón
    def on_mouse_scroll(self,x,y, scroll_x,scroll_y):
        if scroll_y > 0:
            self.player_sprite.objeto_siguiente()
        elif scroll_y < 0:
            self.player_sprite.objeto_anterior()

def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    # Cambiamos MainMenu por TitleView
    menu_view = TitleView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).parent.parent
    print(f"Project root is: {PROJECT_ROOT}")
    main()