import arcade
import os

class GameOverView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.manager = arcade.gui.UIManager()

        fondos = os.path.join('assets', 'fondos') #Cambiar a otro o lo que querais.
        botones = os.path.join('assets', 'botones') #Cambiar a otro o lo que querais.
        self.background = arcade.load_texture(os.path.join(fondos, 'game_over.png'))
        #Lo cambiamos a un nuevo boton
        self.tex_reiniciar = arcade.load_texture(os.path.join(botones, 'boton_reiniciar.png'))
        self.tex_salir = arcade.load_texture(os.path.join(botones, 'boton_cerrar.png'))
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
        retry_btn = arcade.gui.UITextureButton(
            texture=self.tex_reiniciar,
            width=300,
            height=100
        )
        
        # Botón CERRAR JUEGO
        btn_salir = arcade.gui.UITextureButton(
            texture=self.tex_salir,
            width=100,
            height=50
        )

        menu_btn = arcade.gui.UITextureButton(
            texture=self.tex_menu,
            width=300,
            height=100
        )

        v_box.add(retry_btn)
        v_box.add(menu_btn)
        
        # --- EVENTOS DE LOS BOTONES ---
        @retry_btn.event("on_click")
        def on_click_retry(event):
            self.manager.disable()

            from habitaciones import HABITACIONES
            for sala in HABITACIONES:
                sala.nivel_pasado = False

            from views.game_view import GameView
            juego_reiniciado = GameView()

            juego_reiniciado.nombre_partida = self.game_view.nombre_partida
            juego_reiniciado.dificultad = self.game_view.dificultad
            juego_reiniciado.tiempo_jugado = 0.0

            juego_reiniciado.setup(room_id=0)
            juego_reiniciado.guardar_partida()
            self.window.show_view(juego_reiniciado)

        @btn_salir.event("on_click")
        def on_click_salir(event):
            #Quitamos cualquier música que esté sonando
            if hasattr(self.window, "bgm_player") and self.window.bgm_player:
                self.window.bgm_player.delete()
            self.window.close() 
            arcade.exit()
        
        @menu_btn.event("on_click")
        def on_click_menu(event):
            self.manager.disable()
            # Reseteamos las habitaciones
            from habitaciones import HABITACIONES
            for sala in HABITACIONES:
                sala.nivel_pasado = False

            #SOBREESCRITURA DEL JSON EN DISCO (Reset de seguridad)
            from views.game_view import GameView
            juego_reseteado = GameView()

            # Traspasamos los datos de configuración clave
            juego_reseteado.nombre_partida = self.game_view.nombre_partida
            juego_reseteado.dificultad = self.game_view.dificultad
            juego_reseteado.tiempo_jugado = 0.0  # Volvemos a poner el cronómetro a cero

            # Inicializamos y forzamos el guardado en el archivo
            juego_reseteado.setup(room_id=0)
            juego_reseteado.guardar_partida()

            from views.title import TitleView
            nuevo_juego = TitleView()
            self.window.show_view(nuevo_juego)

        anchor.add(
                child=btn_salir, 
                anchor_x="right", 
                anchor_y="top", 
                align_x=-20, 
                align_y=-20
        )

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