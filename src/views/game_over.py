import arcade
import os


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        graficos = os.path.join('assets', 'graphics') #Cambiar a otro o lo que querais.
        botones = os.path.join('assets', 'botones') #Cambiar a otro o lo que querais.
        self.background = arcade.load_texture(os.path.join(graficos, 'fondo_menu.png'))
        #Lo cambiamos a un nuevo boton
        self.tex_reiniciar = arcade.load_texture(os.path.join(botones, 'boton_ajustes.png'))
        self.tex_salir = arcade.load_texture(os.path.join(botones, 'boton_pantalla_completa.png'))
    
    def on_show_view(self):
        self.manager.enable()
        self.setup_gui()
    
    def on_hide_view(self):
        self.manager.disable()
    
    def setup_gui(self):
        self.manager.clear()
        
        anchor = arcade.gui.UIAnchorLayout()
        v_box = arcade.gui.UIBoxLayout(space_between = 10)

        # Botón REINICIAR PARTIDA
        retry_button = arcade.gui.UITextureButton(
            texture=self.tex_reiniciar,
            width=300,
            height=150
        )
        
        # Botón CERRAR JUEGO
        exit_button = arcade.gui.UITextureButton(
            texture=self.tex_salir,
            width=300,
            height=150
        )

        v_box.add(retry_button)
        v_box.add(exit_button)

        # --- EVENTOS DE LOS BOTONES ---
        @retry_button.event("on_click")
        def on_click_retry(event):
            self.manager.disable()
            from views.game_view import GameView
            # Creamos una vista de juego totalmente nueva desde cero
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        @exit_button.event("on_click")
        def on_click_exit(event):
            # Finalizamos el juego
            self.window.close()

        anchor.add(
            child=v_box, 
            anchor_x="center", 
            anchor_y="center", 
            align_y=-60
        )
        self.manager.add(anchor)

    def on_draw(self):
        self.clear()
        # Dibujamos el fondo negro o la imagen de Game Over
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.LRBT(0, self.window.width, 0, self.window.height)
        )
        self.manager.draw()