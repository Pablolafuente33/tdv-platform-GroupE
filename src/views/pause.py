import arcade
import os

class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        # Guardamos la partida actual para no perder el progreso
        self.game_view = game_view
        self.manager = arcade.gui.UIManager()
        
        # Cargamos los gráficos (reutilizando los que ya tienes)
        fondos = os.path.join('assets', 'fondos')
        botones = os.path.join('assets', 'botones')
        self.background = arcade.load_texture(os.path.join(fondos, 'pausa.png'))
        self.tex_reanudar = arcade.load_texture(os.path.join(botones, 'boton_jugar.png'))
        self.tex_reiniciar = arcade.load_texture(os.path.join(botones, 'boton_reiniciar.png')) 
        self.tex_volumen = arcade.load_texture(os.path.join(botones, 'boton_volumen.png'))
        self.guardar_partida = arcade.load_texture(os.path.join(botones, 'boton_guardar_partida.png'))
        self.menu = arcade.load_texture(os.path.join(botones, 'boton_menu.png'))
        self.back_button= arcade.load_texture(os.path.join(botones, 'boton_volver.png'))
        self.tex_cerrar= arcade.load_texture(os.path.join(botones, 'boton_cerrar.png'))
    
    def on_show_view(self):
        self.window.ctx.viewport = (0, 0, self.window.width, self.window.height)
        self.window.ctx.projection_2d = (0, self.window.width, 0, self.window.height)
        self.manager.enable()
        self.setup_gui()

    def on_hide_view(self):
        self.manager.disable()
    
    def setup_gui(self):
        self.manager.clear()
        
        anchor = arcade.gui.UIAnchorLayout()
        v_box = arcade.gui.UIBoxLayout(space_between=0)

        # --- FILA DE VOLUMEN (Horizontal) ---
        h_box_volume = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        vol_label = arcade.gui.UITextureButton(texture=self.tex_volumen, width=200, height=90)
        
        # Sacamos el volumen actual que tenga el reproductor de la ventana
        volumen_global = 20
        if hasattr(self.window, "bgm_player") and self.window.bgm_player:
            volumen_global = int(self.window.bgm_player.volume * 100)

        self.volume_slider = arcade.gui.UISlider(value=volumen_global, width=250)
        h_box_volume.add(vol_label)
        h_box_volume.add(self.volume_slider)

        # BOTONES
        resume_btn = arcade.gui.UITextureButton(
            texture=self.tex_reanudar, 
            width=250, 
            height=125)
        btn_back = arcade.gui.UITextureButton(
            texture=self.back_button,
            texture_hovered=self.back_button,
            text="",
            width=100, 
            height=60)
        retry_btn = arcade.gui.UITextureButton(
            texture=self.tex_reiniciar, 
            width=375, 
            height=100)
        guardar_btn = arcade.gui.UITextureButton(
            texture = self.guardar_partida,
            width=325, 
            height=100)
        menu_btn = arcade.gui.UITextureButton(
            texture = self.menu,
            width=275, 
            height=115)

        # Los añadimos al contenedor vertical
        v_box.add(h_box_volume)
        v_box.add(resume_btn)
        v_box.add(retry_btn)
        v_box.add(guardar_btn)
        v_box.add(menu_btn)
        
        # --- EVENTOS ---
        
        @self.volume_slider.event("on_change")
        def on_volume_change(event):
            vol = self.volume_slider.value / 100
            if hasattr(self.window, "bgm_player") and self.window.bgm_player:
                self.window.bgm_player.volume = vol

        @resume_btn.event("on_click")
        @btn_back.event("on_click")
        def on_click_resume(event):
            self.manager.disable()
            #Volvemos a donde estábamos
            self.game_view.camera.use()
            self.window.show_view(self.game_view)
        
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

        @guardar_btn.event("on_click")
        def on_click_guardar(event):
            self.game_view.guardar_partida()
        
        @menu_btn.event("on_click")
        def on_click_menu(event):
            self.manager.disable()
            
            from views.title import TitleView
            nuevo_juego = TitleView()
            self.window.show_view(nuevo_juego)

        # Centramos todo el panel en pantalla
        anchor.add(
            child=v_box, 
            anchor_x="center", 
            anchor_y="center",
            align_y=-100
        )
        # lo ponemos en la esquina superior izquierda
        anchor.add(
            child=btn_back,
            anchor_x="left",
            anchor_y="top",
            align_x=20,   
            align_y=-40   
        )

        # Para cerrar el juego desde la pausa
        btn_salir = arcade.gui.UITextureButton(texture = self.tex_cerrar, width=100, height=60)
        
        @btn_salir.event("on_click")
        def on_click_salir(event):
            #Quitamos cualquier música que esté sonando
            if hasattr(self.window, "bgm_player") and self.window.bgm_player:
                self.window.bgm_player.delete()
            self.window.close() 
            arcade.exit()

        anchor.add(
                child=btn_salir, 
                anchor_x="right", 
                anchor_y="top", 
                align_x=-20, 
                align_y=-20
        )

        self.manager.add(anchor)

    def on_draw(self):
        self.clear()
        # Dibujamos tu fondo medieval estirado al tamaño real actual de la ventana
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.LRBT(0, self.window.width, 0, self.window.height)
        )
        
        # Dibujamos los botones del UIManager en el nuevo centro calculado
        self.manager.draw()

    #Si le damos a escape también volvemos a donde estábamos 
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.manager.disable()
            self.window.show_view(self.game_view)