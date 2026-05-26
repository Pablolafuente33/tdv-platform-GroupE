import arcade
import arcade.gui
import os

from views.game_view import GameView


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
            self.window.volumen_guardado = 0.2
            if hasattr(self.window, "bgm_player") and self.window.bgm_player:
                self.window.volumen_guardado = self.window.bgm_player.volume
                self.window.bgm_player.delete()
                self.window.bgm_player = None

            self.window.current_bgm_track = None

            game_view = GameView()
            game_view.setup()  # Inicializa el mapa, jugador, etc.
            self.window.show_view(game_view)

        @settings_button.event("on_click")
        def on_click_settings(event):
            self.manager.disable()

            from views.setting import SettingsView

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
                    right=self.window.width, 
                    bottom=0, 
                    top=self.window.height   
                )
            )
            self.manager.draw()