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
        fondos = os.path.join('assets', 'fondos')
        botones = os.path.join('assets', 'botones')
        self.background = arcade.load_texture(os.path.join(fondos, 'menu.png'))
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
        
        self.v_box = arcade.gui.UIBoxLayout(space_between=0)

        # Creación del botón de CARGAR_PARTIDA
        cargar_button = arcade.gui.UITextureButton(
            texture=self.cargar_button,
            texture_hovered=self.cargar_button,
            texture_pressed=self.cargar_button,
            text="", 
            width=350,
            height=150
        )
        
        #Creación del botón de NUEVA_PARTIDA
        nueva_partida_button = arcade.gui.UITextureButton(
            texture=self.nueva_partida_button,
            texture_hovered=self.nueva_partida_button,
            texture_pressed=self.nueva_partida_button,
            text="", 
            width=350,
            height=150
        )

        # Creación del botón de AJUSTES
        settings_button = arcade.gui.UITextureButton(
            texture=self.tex_ajustes,
            texture_hovered=self.tex_ajustes,
            texture_pressed=self.tex_ajustes,
            text="",
            width=300,
            height=150
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
            self.manager.disable()

            from views.charge_game import ChargeGameview

            self.window.show_view(ChargeGameview())
            
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
            align_y=-100
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