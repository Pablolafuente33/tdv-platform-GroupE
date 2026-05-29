import arcade
import os

from views.title import TitleView

class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        
        fondos = os.path.join('assets', 'fondos')
        botones = os.path.join('assets', 'botones')
        
        self.background = arcade.load_texture(os.path.join(fondos, 'ajustes.png'))
        self.tex_volumen = arcade.load_texture(os.path.join(botones, 'boton_volumen.png'))
        self.tex_pantalla = arcade.load_texture(os.path.join(botones, 'boton_pantalla_completa.png'))
        self.tex_volver = arcade.load_texture(os.path.join(botones, 'boton_volver.png'))


    def on_show_view(self):
        self.manager.enable()
        self.setup_gui()


    def on_resize(self, width, height):
        self.window.ctx.projection_2d = (0, width, 0, height)
        self.setup_gui()

    def setup_gui(self):
        self.manager.clear()
        
        anchor = arcade.gui.UIAnchorLayout()
        
        v_box = arcade.gui.UIBoxLayout(space_between=0)

        # --- FILA DE VOLUMEN (Horizontal) ---
        h_box_volume = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        
        vol_label = arcade.gui.UITextureButton(
            texture=self.tex_volumen, 
            width=250, 
            height=150
        )
        
        volumen_global = 20
        if hasattr(self.window, "bgm_player") and self.window.bgm_player:
            volumen_global = int(self.window.bgm_player.volume * 100)

        self.volume_slider = arcade.gui.UISlider(value=volumen_global, width=300)
        
        h_box_volume.add(vol_label)
        h_box_volume.add(self.volume_slider)

        # --- BOTONES ---
        fullscreen_btn = arcade.gui.UITextureButton(
            texture=self.tex_pantalla, 
            width=300, 
            height=200
        )

        back_btn = arcade.gui.UITextureButton(
            texture=self.tex_volver,
            width=100,
            height=60
        )

        # --- EVENTOS ---
        @self.volume_slider.event("on_change")
        def on_volume_change(event):
            vol = self.volume_slider.value / 100
            if hasattr(self.window, "bgm_player") and self.window.bgm_player:
                self.window.bgm_player.volume = vol

        @fullscreen_btn.event("on_click")
        def on_click_fullscreen(event):
            self.window.set_fullscreen(not self.window.fullscreen)
            self.on_resize(self.window.width, self.window.height)

        @back_btn.event("on_click")
        def on_click_back(event):
            self.manager.disable()
            self.window.show_view(TitleView())

        # --- AGREGAR AL CONTENEDOR PRINCIPAL ---
        v_box.add(h_box_volume)
        v_box.add(fullscreen_btn)

        anchor.add(
            child=v_box, 
            anchor_x="center", 
            anchor_y="center",
            align_y=-100 
        )

        #Metemos el boton de volver arriba a la izquierda
        anchor.add(
            child=back_btn,
            anchor_x="left",
            anchor_y="top",
            align_x=20,   
            align_y=-20   
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

    def on_hide_view(self):
        self.manager.disable()