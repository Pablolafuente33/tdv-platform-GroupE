import arcade
import arcade.gui
import os
import sys

class VictoryView(arcade.View):
    def __init__(self, nombre_partida, tiempo_jugado, dificultad):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        self.nombre_partida = nombre_partida
        self.dificultad = dificultad

        minutos = int(tiempo_jugado // 60)
        segundos = int(tiempo_jugado % 60)
        self.tiempo = f"{minutos:02d} : {segundos:02d}"

        fondos = os.path.join('assets', 'fondos')
        botones = os.path.join('assets', 'botones')

        self.background = arcade.load_texture(os.path.join(fondos, 'victoria.png'))
        self.tex_menu = arcade.load_texture(os.path.join(botones, 'boton_menu.png'))
        self.tex_cerrar =  arcade.load_texture(os.path.join(botones, 'boton_cerrar.png'))
        
        self.music = arcade.load_sound(os.path.join('assets', 'music', 'VictorySound.mp3'),
                                       streaming= True)
        self.fuente = arcade.load_font(os.path.join('assets','fuente','BlackCastleMF.ttf' ))


    def on_show_view(self):
        self.manager.enable()
        self.setup_gui()
        volumen_actual = getattr(self.window, "volumen_guardado", 0.2)
        
        # Comprobamos que no esté sonando ya la de victoria para no duplicarla
        if not hasattr(self.window, "current_bgm_track") or self.window.current_bgm_track != "victory":
            # Quitar música que estuviera sonando
            if hasattr(self.window, "bgm_player") and self.window.bgm_player:
                self.window.bgm_player.delete()
                
                # Lanzamos el tema de victoria en bucle
                self.window.bgm_player = self.music.play(loop=True, volume=volumen_actual)
                self.window.current_bgm_track = "victory"
        
    def on_hide_view(self):
            self.manager.disable()

    def setup_gui(self):
            self.manager.clear()
            anchor = arcade.gui.UIAnchorLayout()

            v_box = arcade.gui.UIBoxLayout(space_between=10)

            texto_estadisticas = (
                f"HÉROE: {self.nombre_partida.upper()}\n\n"
                f"DIFICULTAD SUPERADA: {self.dificultad}\n\n"
                f"TIEMPO TOTAL DE JUEGO: {self.tiempo}"
            )

            cuadro_stats = arcade.gui.UITextArea(
                text=texto_estadisticas,
                width=500,
                height=140,
                text_color=arcade.color.ORANGE_PEEL,
                font_size=18,
                font_name="BlackCastleMF"
            )
            v_box.add(cuadro_stats)

            v_box.add(arcade.gui.UISpace(height=20))

            btn_menu = arcade.gui.UITextureButton(
                texture = self.tex_menu,
                width=280,
                height=150
            )

            @btn_menu.event("on_click")
            def on_click_menu(event):
                # Limpiamos hilos de música por si acaso
                if hasattr(self.window, "bgm_player") and self.window.bgm_player:
                    self.window.bgm_player.delete()
                    self.window.bgm_player = None
                if hasattr(self.window, "current_bgm_track"):
                    self.window.current_bgm_track = None
                    
                from views.title import TitleView
                self.window.show_view(TitleView())
            
            v_box.add(btn_menu) 

            btn_salir = arcade.gui.UITextureButton(texture = self.tex_cerrar, width=100, height=50)
        
            @btn_salir.event("on_click")
            def on_click_salir(event):
                #Quitamos cualquier música que esté sonando
                if hasattr(self.window, "bgm_player") and self.window.bgm_player:
                    self.window.bgm_player.delete()
                self.window.close() 
                sys.exit()


            anchor.add(
                child=v_box, 
                anchor_x="center",
                anchor_y="center", 
                align_y=-100
            )
            
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
        # Renderizamos el tapiz de fondo del grupo
        arcade.draw_texture_rect(
            texture=self.background,
                rect=arcade.LRBT(0, self.window.width, 0, self.window.height)
            )
        self.manager.draw()

