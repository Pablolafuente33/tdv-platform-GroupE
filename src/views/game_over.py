import arcade
import os


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        fondos = os.path.join('assets', 'fondos') #Cambiar a otro o lo que querais.
        botones = os.path.join('assets', 'botones') #Cambiar a otro o lo que querais.
        self.background = arcade.load_texture(os.path.join(fondos, 'game_over.png'))
        #Lo cambiamos a un nuevo boton
        self.tex_reiniciar = arcade.load_texture(os.path.join(botones, 'boton_reiniciar.png'))
        self.tex_salir = arcade.load_texture(os.path.join(botones, 'boton_pantalla_completa.png'))
        self.tex_menu = arcade.load_texture(os.path.join(botones, 'boton_menu.png'))
    
    def on_show_view(self):
        self.manager.enable()
        self.setup_gui()
    
    def on_hide_view(self):
        self.manager.disable()
    
    def setup_gui(self):
        self.manager.clear()
        
        anchor = arcade.gui.UIAnchorLayout()
        v_box = arcade.gui.UIBoxLayout(space_between = 5)

        # Botón REINICIAR PARTIDA
        retry_button = arcade.gui.UITextureButton(
            texture=self.tex_reiniciar,
            width=300,
            height=100
        )
        
        # Botón CERRAR JUEGO
        exit_button = arcade.gui.UITextureButton(
            texture=self.tex_salir,
            width=300,
            height=150
        )

        menu_button = arcade.gui.UITextureButton(
            texture=self.tex_menu,
            width=300,
            height=100
        )

        v_box.add(retry_button)
        v_box.add(menu_button)
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
            align_y=-100
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