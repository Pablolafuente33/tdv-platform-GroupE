import arcade
import os


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        # Guardamos la partida actual para no perder el progreso
        self.game_view = game_view
        self.manager = arcade.gui.UIManager()
        
        # Cargamos los gráficos (reutilizando los que ya tienes)
        graficos = os.path.join('assets', 'graphics')
        self.background = arcade.load_texture(os.path.join(graficos, 'fondo_menu.png'))
        self.tex_reanudar = arcade.load_texture(os.path.join(graficos, 'boton_jugar.png'))
        self.tex_pantalla = arcade.load_texture(os.path.join(graficos, 'boton_pantalla_completa.png'))
        self.tex_reiniciar = arcade.load_texture(os.path.join(graficos, 'boton_ajustes.png')) 
        self.tex_volumen = arcade.load_texture(os.path.join(graficos, 'boton_volumen.png'))

    def on_show_view(self):
        self.window.ctx.viewport = (0, 0, self.window.width, self.window.height)
        self.window.ctx.projection_2d = (0, self.window.width, 0, self.window.height)
        self.manager.enable()
        self.setup_gui()

    def on_hide_view(self):
        self.manager.disable()
    
    def on_resize(self, width, height):
        print(f"[PauseView] on_resize llamado: {width}x{height}")
        self.window.ctx.projection_2d = (0, width, 0, height)
        self.setup_gui()
    
    def setup_gui(self):
        self.manager.clear()
        
        anchor = arcade.gui.UIAnchorLayout()
        v_box = arcade.gui.UIBoxLayout(space_between=10)

        # --- FILA DE VOLUMEN (Horizontal) ---
        h_box_volume = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        vol_label = arcade.gui.UITextureButton(texture=self.tex_volumen, width=200, height=100)
        
        # Sacamos el volumen actual que tenga el reproductor de la ventana
        volumen_global = 20
        if hasattr(self.window, "bgm_player") and self.window.bgm_player:
            volumen_global = int(self.window.bgm_player.volume * 100)

        self.volume_slider = arcade.gui.UISlider(value=volumen_global, width=250)
        h_box_volume.add(vol_label)
        h_box_volume.add(self.volume_slider)

        # --- BOTONES PRINCIPALES ---
        resume_btn = arcade.gui.UITextureButton(
            texture=self.tex_reanudar, 
            width=250, 
            height=125)
        fullscreen_btn = arcade.gui.UITextureButton(
            texture=self.tex_pantalla, 
            width=250, 
            height=125)
        retry_btn = arcade.gui.UITextureButton(
            texture=self.tex_reiniciar, 
            width=250, 
            height=125)

        # Los añadimos al contenedor vertical
        v_box.add(h_box_volume)
        v_box.add(resume_btn)
        v_box.add(fullscreen_btn)
        v_box.add(retry_btn)

        # --- EVENTOS ---
        
        @self.volume_slider.event("on_change")
        def on_volume_change(event):
            vol = self.volume_slider.value / 100
            if hasattr(self.window, "bgm_player") and self.window.bgm_player:
                self.window.bgm_player.volume = vol

        @resume_btn.event("on_click")
        def on_click_resume(event):
            self.manager.disable()
            #Volvemos a donde estábamos
            self.game_view.camera.use()
            self.window.show_view(self.game_view)

        @fullscreen_btn.event("on_click")        
        def on_click_fullscreen(event):
            self.window.set_fullscreen(not self.window.fullscreen)
            self.on_resize(self.window.width, self.window.height)
        
        @retry_btn.event("on_click")
        def on_click_retry(event):
            self.manager.disable()
            # Creamos una partida completamente nueva desde cero

            from views.title import TitleView
            nuevo_juego = TitleView()
            nuevo_juego.setup()
            self.window.show_view(nuevo_juego)

        # Centramos todo el panel en pantalla
        anchor.add(
            child=v_box, 
            anchor_x="center", 
            anchor_y="center",
            align_y=-40
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