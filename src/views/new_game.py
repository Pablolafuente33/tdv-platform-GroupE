import arcade
import arcade.gui
import os
import sys

class NewGameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        
        # Cargamos el mismo fondo que uséis en los menús
        fondos = os.path.join('assets', 'fondos')
        botones = os.path.join('assets', 'botones') 
        self.background = arcade.load_texture(os.path.join(fondos, 'nueva_partida.png'))
        self.tex_jugar = arcade.load_texture(os.path.join(botones,'boton_jugar.png'))
        self.dificil_button = arcade.load_texture(os.path.join(botones,'boton_dificil.png'))
        self.normal_button = arcade.load_texture(os.path.join(botones,'boton_normal.png'))
        self.facil_button = arcade.load_texture(os.path.join(botones,'boton_facil.png'))
        self.back_button = arcade.load_texture(os.path.join(botones, 'boton_volver.png'))
        self.tex_cerrar = arcade.load_texture(os.path.join(botones, 'boton_cerrar.png'))
        self.dificultad = "Normal"
        
        self.fuente = arcade.load_font(os.path.join('assets','fuente','BlackCastleMF.ttf' ))

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
        v_box = arcade.gui.UIBoxLayout(space_between=0)

        # 1. Añadimos una etiqueta de texto que guíe al jugador
        label = arcade.gui.UILabel(
            text="Introduzca el nombre de la partida:",
            width=550,
            height=35,
            text_color=arcade.color.ORANGE_PEEL,
            font_size=25,
            font_name="BlackCastleMF"
        )
        v_box.add(label)

        #Creamos un cuadro par que se escriba el nombre de la partida.
        self.input_nombre = arcade.gui.UIInputText(
            text="Partida1",  
            width=300,
            height= 40,
            text_color=arcade.color.ORANGE_PEEL,
            font_size = 22,
            font_name="BlackCastleMF"
        )
        
        v_box.add(self.input_nombre)

        v_box.add(arcade.gui.UISpace(height=20))

        #Para determinar la dificultad de la partida:
        dificultad_label = arcade.gui.UILabel(
            text="Seleccionar dificultad",
            width = 400,
            height = 28,
            text_color = arcade.color.ORANGE_PEEL,
            font_size = 25,
            font_name="BlackCastleMF"
        )
        v_box.add(dificultad_label)

        #Creamos el compartimiento donde van a estar las etiquetas de las dificultades
        dificultad_box = arcade.gui.UIBoxLayout(
            vertical=False,
            space_between=5
        )

        btn_facil = arcade.gui.UITextureButton(
            texture = self.facil_button,
        )

        btn_normal = arcade.gui.UITextureButton(
            texture = self.normal_button,
        )

        btn_dificil = arcade.gui.UITextureButton(
            texture = self.dificil_button,
        )

        dificultad_box.add(btn_facil)
        dificultad_box.add(btn_normal)
        dificultad_box.add(btn_dificil)

        v_box.add(dificultad_box)
        # --- SISTEMA DE VISUALIZACIÓN CLARA DE DIFICULTAD ---
        def actualizar_botones_dificultad():
            for btn in [btn_facil, btn_normal, btn_dificil]:
                btn.width = 220
                btn.height = 130

            # El botón que ha sido activado lo hacemos más grande
            if self.dificultad == "Facil":
                btn_facil.width = 270
                btn_facil.height = 190
            elif self.dificultad == "Normal":
                btn_normal.width = 270
                btn_normal.height = 190
            elif self.dificultad == "Dificil":
                btn_dificil.width = 270
                btn_dificil.height = 190
            
            self.manager.trigger_render()
        
        actualizar_botones_dificultad()
                
        @btn_facil.event("on_click")
        def on_click_facil(event):
            self.dificultad = "Facil"
            print("Dificultad seleccionada: Fácil")
            actualizar_botones_dificultad()

        @btn_normal.event("on_click")
        def on_click_normal(event):
            self.dificultad = "Normal"
            print("Dificultad seleccionada: Normal")
            actualizar_botones_dificultad()

        @btn_dificil.event("on_click")
        def on_click_dificil(event):
            self.dificultad = "Dificil"
            print("Dificultad seleccionada: Difícil")
            actualizar_botones_dificultad()
    
        # Botón para empezar a jugar
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
                nombre_partida = "Partida1"

            #Contruimos el archivo donde se va a guardar la parrtida
            nombre_archivo = f'{nombre_partida}.json'
            ruta = os.path.join("saves", nombre_archivo)
            #Debemos de mirar que no hay otra partida con el mismo nombre
            if os.path.exists(ruta):
                #Lanzamos un mensaje de aviso
                label.text = "¡ESE NOMBRE DE PARTIDA YA EXISTE! Elige otro:"
                label.text_color = arcade.color.RED
                label.font_name = "BlackCastleMF"
                return
            
            if os.path.exists("saves"):
                partidas_guardadas = [f
                    for f in os.listdir("saves")
                        if f.endswith('.json') ]
                if len(partidas_guardadas) >= 5 :
                    rutas = [os.path.join("saves", f) 
                                for f in partidas_guardadas]
                    
                    partida_vieja= min(rutas, key = os.path.getmtime)

                    try:
                        borrado = os.path.basename(partida_vieja).replace(".json", "")
                        os.remove(partida_vieja)
                        print(f'Máximo de partidas guardadas alcanzado.\nSe ha eliminado la partida más vieja:{borrado}')
                    except Exception as e:
                        print(f'Error al borrar el archivo más antiguo: {e}')
            # Lanzamos el juego
            from views.game_view import GameView
            juego_view = GameView()
            
            # Asignamos el nombre a la partida antes de mostrarla
            juego_view.nombre_partida = nombre_partida
            juego_view.tiempo_total_jugado = 0.0
            juego_view.dificultad = self.dificultad
            juego_view.setup()
            juego_view.guardar_partida()
            self.window.show_view(juego_view)

        anchor.add(child=v_box, 
                   anchor_x="center", 
                   anchor_y="center", 
                   align_y=-130)

        btn_back = arcade.gui.UITextureButton(
            texture=self.back_button,
            texture_hovered=self.back_button,
            text="",
            width=100, 
            height=60
        )

        # Evento para regresar al menú principal 
        @btn_back.event("on_click")
        def on_click_back(event):
            from views.title import TitleView  
            self.window.show_view(TitleView())

        # lo ponemos en la esquina superior izquierda
        anchor.add(
            child=btn_back,
            anchor_x="left",
            anchor_y="top",
            align_x=20,   
            align_y=-20   
        )

        btn_salir = arcade.gui.UITextureButton(texture = self.tex_cerrar, width=100, height=50)
        
        @btn_salir.event("on_click")
        def on_click_salir(event):
            #Quitamos cualquier música que esté sonando
            if hasattr(self.window, "bgm_player") and self.window.bgm_player:
                self.window.bgm_player.delete()
            self.window.close() 
            sys.exit()
        
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
        # Dibujamos el fondo
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.LRBT(0, self.window.width, 0, self.window.height)
        )
        self.manager.draw()