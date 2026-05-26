import arcade
import arcade.gui
import os

class NewGameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        
        # Cargamos el mismo fondo que uséis en los menús
        graficos = os.path.join('assets', 'graphics')
        botones = os.path.join('assets', 'botones') 
        self.background = arcade.load_texture(os.path.join(graficos, 'fondo_ajustes.png'))
        self.tex_jugar = arcade.load_texture(os.path.join(botones,'boton_jugar.png'))
        self.dificil_button = arcade.load_texture(os.path.join(botones,'boton_dificil.png'))
        self.normal_button = arcade.load_texture(os.path.join(botones,'boton_normal.png'))
        self.facil_button = arcade.load_texture(os.path.join(botones,'boton_facil.png'))
        self.dificultad = 'Normal'
        # Guardaremos el cuadro de texto en una variable de clase para leerlo luego
        self.input_nombre = None

    def on_show_view(self):
        self.manager.enable()
        self.setup_gui()

    def on_hide_view(self):
        self.manager.disable()

    def setup_gui(self):
        self.manager.clear()
        
        anchor = arcade.gui.UIAnchorLayout()
        v_box = arcade.gui.UIBoxLayout(space_between=3)

        # 1. Añadimos una etiqueta de texto que guíe al jugador
        label = arcade.gui.UITextWidget(
            text="Introduce el nombre de la partida:",
            width=300,
            height=40,
            text_color=arcade.color.WHITE,
            font_size = 20
        )
        v_box.add(label)

        #Creamos un cuadro par que se escriba el nombre de la partida.
        self.input_nombre = arcade.gui.UIInputText(
            text="Partida1",  # Nombre por defecto
            width=300,
            height=40,
            text_color=arcade.color.ORANGE_PEEL
        )
        
        v_box.add(self.input_nombre)
        #Para determinar la dificultad de la partida:
        dificultad_label = arcade.gui.UITextWidget(
            text="Seleccionar dificultad",
            width = 300,
            height = 40,
            text_color = arcade.color.WHITE,
            font_size = 20
        )
        v_box.add(dificultad_label)

        #Creamos el compartimiento donde van a estar las etiquetas de las dificultades
        dificultad_box = arcade.gui.UIBoxLayout(
            vertical=False,
            space_between=10
        )

        btn_facil = arcade.gui.UITextureButton(
            texture = self.facil_button,
            texture_hovered=self.facil_button,
            text="",
            width = 250,
            height=175
        )

        btn_normal = arcade.gui.UITextureButton(
            texture = self.normal_button,
            texture_hovered= self.normal_button,
            text="",
            width = 250,
            height=175
        )

        btn_dificil = arcade.gui.UITextureButton(
            texture = self.dificil_button,
            texture_hovered = self.dificil_button,
            text="",
            width = 250,
            height=175
        )

        dificultad_box.add(btn_facil)
        dificultad_box.add(btn_normal)
        dificultad_box.add(btn_dificil)

        v_box.add(dificultad_box)

        @btn_facil.event("on_click")
        def on_click_facil(event):
            self.dificultad = "Fácil"

            print("Dificultad seleccionada: Fácil")

        @btn_normal.event("on_click")
        def on_click_normal(event):
            self.dificultad = "Normal"

            print("Dificultad seleccionada: Normal")

        @btn_dificil.event("on_click")
        def on_click_dificil(event):
            self.dificultad = "Difícil"

            print("Dificultad seleccionada: Difícil")

        # 3. Botón para confirmar y empezar
        tex_jugar = arcade.gui.UITextureButton(
            texture = self.tex_jugar,
            texture_hovered=self.tex_jugar,
            text="",
            height=175, 
            width=250
        )
        v_box.add(tex_jugar)

        # --- EVENTO DEL BOTÓN CONFIRMAR ---
        @tex_jugar.event("on_click")
        def on_click_jugar(event):
            # Extraemos el texto que ha escrito el usuario
            nombre_partida = self.input_nombre.text.strip()
            
            if not nombre_partida:
                nombre_partida = "Parida1"

            # Avanzamos al GameView pasando el nombre
            from views.game_view import GameView
            juego_view = GameView()
            
            # Asignamos el nombre a la partida antes de mostrarla
            juego_view.nombre_partida = nombre_partida
            juego_view.tiempo_total_jugado = 0.0
            juego_view.setup()
            self.window.show_view(juego_view)

        anchor.add(child=v_box, anchor_x="center", anchor_y="center", align_y=-50)
        self.manager.add(anchor)

    def on_draw(self):
        self.clear()
        # Dibujamos el fondo
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.LRBT(0, self.window.width, 0, self.window.height)
        )
        self.manager.draw()