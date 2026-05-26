import arcade
import arcade.gui
import os
import json

from views.game_view import GameView


class TitleView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        
        # Cargamos las imágenes del fondo y los botones
        graficos = os.path.join('assets', 'graphics')
        botones = os.path.join('assets', 'botones')
        self.background = arcade.load_texture(os.path.join(graficos, 'fondo_menu.png'))
        self.tex_ajustes = arcade.load_texture(os.path.join(botones,'boton_ajustes.png'))
        self.cargar_button = arcade.load_texture(os.path.join(botones,'boton_cargar_partida.png'))
        self.nueva_partida_button = arcade.load_texture(os.path.join(botones,'boton_nueva_partida.png'))
        #Musica de inicio
        self.load_music = arcade.load_sound(os.path.join('assets','music','InitSound.mp3'), streaming= True)

    def on_show_view(self):
        self.manager.enable()
        self.setup_gui()
        
        volumen_actual = 0.2
        if hasattr(self.window, "bgm_player") and self.window.bgm_player:
            volumen_actual = self.window.bgm_player.volume

        if not hasattr(self.window, "current_bgm_track") or self.window.current_bgm_track != "menu":
            if hasattr(self.window, "bgm_player") and self.window.bgm_player:
                self.window.bgm_player.delete()
            
            self.window.bgm_player = self.load_music.play(loop=True, volume=volumen_actual)
            self.window.current_bgm_track = "menu"

    def on_hide_view(self):
        self.manager.disable()

    def on_resize(self, width, height):
            # Reajusta la proyección 2D para que el dibujo no se estire
            self.window.ctx.projection_2d = (0, width, 0, height)
            # Reposiciona los botones del menú al nuevo centro
            self.setup_gui()

    def setup_gui(self):
        self.manager.clear()
        
        anchor = arcade.gui.UIAnchorLayout()
        
        self.v_box = arcade.gui.UIBoxLayout(space_between=3)

        # Creación del botón de CARGAR_PARTIDA
        cargar_button = arcade.gui.UITextureButton(
            texture=self.cargar_button,
            texture_hovered=self.cargar_button,
            texture_pressed=self.cargar_button,
            text="", 
            width=350,
            height=175
        )
        
        #Creación del botón de NUEVA_PARTIDA
        nueva_partida_button = arcade.gui.UITextureButton(
            texture=self.nueva_partida_button,
            texture_hovered=self.nueva_partida_button,
            texture_pressed=self.nueva_partida_button,
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

        self.v_box.add(cargar_button)
        self.v_box.add(nueva_partida_button)
        self.v_box.add(settings_button)
        

        # Eventos al hacer click en los botones

        
        @settings_button.event("on_click")
        def on_click_settings(event):
            self.manager.disable()

            from views.setting import SettingsView

            self.window.show_view(SettingsView())

        @cargar_button.event("on_click")
        def on_click_cargar(event):
            os.makedirs('saves', exist_ok = True)

            archivos_guardados = [ archivo
                                  for archivo in os.listdir('saves')
                                  if archivo.endswith('.json')]
            
            #Si no hay partidas
            if not archivos_guardados:
                print("No hay partidas guardadas.")
                return

            nombre_archivo = archivos_guardados[0]
            ruta_guardado = os.path.join('saves',nombre_archivo)

            with open(ruta_guardado, 'r', encoding = 'utf-8') as f:
                 datos_cargados = json.load(f)

            # Creamos la vista del juego
            from views.game_view import GameView
            juego_view = GameView()
            
            # --- AQUÍ OCURRE LA MAGIA: Reinyectamos los datos guardados ---
            juego_view.nombre_partida = datos_cargados["nombre_partida"]
            juego_view.tiempo_total_jugado = datos_cargados["tiempo_jugado_segundos"]
            
            # 1. Cargamos la escena/mapa en la que se quedó
            # Tu método para cargar mapas debería aceptar la ruta como parámetro
            juego_view.cargar_mapa(datos_cargados["sala_actual"]) 
            
            # 2. Colocamos al jugador en sus coordenadas y le devolvemos su vida
            juego_view.player_sprite.center_x = datos_cargados["jugador"]["pos_x"]
            juego_view.player_sprite.center_y = datos_cargados["jugador"]["pos_y"]
            juego_view.player_sprite.vida = datos_cargados["jugador"]["vida"]
            
            # 3. Restauramos los jefes derrotados
            juego_view.jefe1_muerto = datos_cargados["jefes_derrotados"]["jefe_1"]

            # Mostramos la vista del juego ya configurada con el pasado del jugador
            self.window.show_view(juego_view)

        @nueva_partida_button.event("on_click")
        def on_click_nueva_partida(event):

            from views.new_game import NewGameView
            nueva_view = NewGameView()

            self.window.show_view(nueva_view)
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
                    right=self.window.width, 
                    bottom=0, 
                    top=self.window.height   
                )
            )
            self.manager.draw()