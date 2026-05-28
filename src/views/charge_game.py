import arcade
import arcade.gui
import os
import json

class ChargeGameview(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        graficos = os.path.join('assets', 'graphics')
        botones = os.path.join('assets', 'botones')

        self.background = arcade.load_texture(os.path.join(graficos, 'cargar_partidas.png'))
        self.tex_jugar = arcade.load_texture(os.path.join(botones, 'boton_jugar.png'))
        self.tex_volver = arcade.load_texture(os.path.join(botones, 'boton_volver.png'))
        

    def on_show_view(self):
        self.manager.enable()
        self.setup_gui()

    def on_hide_view(self):
        self.manager.disable()

    def setup_gui(self):
        self.manager.clear()
        
        anchor = arcade.gui.UIAnchorLayout()
        
        # Contenedor vertical principal
        v_box = arcade.gui.UIBoxLayout(space_between=15)
        
        # Título de la pantalla
        titulo = arcade.gui.UILabel(
            text="SELECCIONAR PARTIDA",
            width=400,
            height=40,
            text_color=arcade.color.ORANGE_PEEL,
            font_size=25,
            font_name="Georgia"
        )
        v_box.add(titulo)
        
        # Contenedor para la lista de partidas encontradas
        lista_partidas_box = arcade.gui.UIBoxLayout(space_between=10)
        
        # --- ESCANEO DE LA CARPETA DE GUARDADOS ---
        carpeta_saves = "saves"
        partidas_encontradas = False
        
        if os.path.exists(carpeta_saves):
            # Listamos los archivos que terminen en .json
            archivos = [f for f in os.listdir(carpeta_saves) if f.endswith('.json')]
            
            for archivo in archivos:
                partidas_encontradas = True
                nombre_partida = archivo.replace(".json", "")
                
                # Creamos un botón plano de texto para seleccionar la partida
                # Puedes usar UITextureButton si prefieres meterle una imagen de pergamino/madera detrás
                btn_partida = arcade.gui.UIFlatButton(
                    text=nombre_partida.upper(),
                    width=300,
                    height=50
                )
                
                # Pasamos el nombre del archivo al evento usando un truco de clausura de Python (archivo=archivo)
                @btn_partida.event("on_click")
                def on_click_cargar(event, archivo_partida=archivo):
                    self.cargar_y_lanzar_partida(archivo_partida)
                    
                lista_partidas_box.add(btn_partida)
                
        if not partidas_encontradas:
            # Mensaje en caso de que no haya ninguna partida grabada
            aviso_vacio = arcade.gui.UILabek(
                text="No se encontraron partidas guardadas.",
                width=400,
                height=35,
                text_color=arcade.color.RED,
                font_size=16,
            )
            lista_partidas_box.add(aviso_vacio)
            
        v_box.add(lista_partidas_box)
        
        # Bajar todo el menú central para que no tape vuestros títulos del fondo
        anchor.add(child=v_box, 
                   anchor_x="center", 
                   anchor_y="center", 
                   align_y=-50)
        
        btn_volver = arcade.gui.UITextureButton(
            texture=self.tex_volver,
            text="",
            width=120,
            height=60
        )
        
        @btn_volver.event("on_click")
        def on_click_volver(event):
            from views.title import TitleView
            self.window.show_view(TitleView())
            
        anchor.add(child=btn_volver, 
                   anchor_x="left", 
                   anchor_y="top", 
                   align_x=20, 
                   align_y=-20)
        
        self.manager.add(anchor)

    def cargar_y_lanzar_partida(self, archivo_json):
        ruta_completa = os.path.join("saves", archivo_json)
        
        try:
            with open(ruta_completa, "r", encoding="utf-8") as f:
                datos = json.load(f)
                
            # 1. Instanciamos el GameView sin arrancar el setup por defecto
            from views.game_view import GameView
            juego_view = GameView()
            
            juego_view.setup(datos_carga = datos)
            
            self.window.show_view(juego_view)
            
        except Exception as e:
            print(f"Error crítico al intentar cargar el archivo {archivo_json}: {e}")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.LRBT(0, self.window.width, 0, self.window.height)
        )
        self.manager.draw()