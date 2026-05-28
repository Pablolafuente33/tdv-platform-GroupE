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
        titulo = arcade.gui.UITextArea(
            text="SELECCIONAR PARTIDA",
            width=400,
            height=40,
            text_color=arcade.color.ORANGE_PEEL,
            font_size=28,
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
            aviso_vacio = arcade.gui.UITextArea(
                text="No se encontraron partidas guardadas.",
                width=400,
                height=35,
                text_color=arcade.color.WHITE,
                font_size=16,
                font_name="Georgia"
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
            
            # 2. Inyectamos los datos básicos del menú
            juego_view.nombre_partida = datos["nombre_partida"]
            juego_view.dificultad_partida = datos["dificultad"]
            juego_view.tiempo_total_jugado = datos["tiempo_jugado_segundos"]
            juego_view.current_room_id = datos["sala_actual"]
            
            # 3. Lanzamos el setup inicial (que carga el mapa Tiled básico)
            juego_view.setup()
            
            # 4. SOBREESCRIBIMOS EL MUNDO CON LOS DATOS DEL JSON
            # Posicionamos al jugador donde se quedó
            juego_view.player_sprite.center_x = datos["jugador"]["pos_x"]
            juego_view.player_sprite.center_y = datos["jugador"]["pos_y"]
            juego_view.player_sprite.health = datos["jugador"]["vida"]
            
            # Recontrucción de la Enemy_list
            from personajes import EsqueletoEnemigo, DuendeEnemigo, CocodriloEnemigo
            
            juego_view.enemy_list.clear() # Limpiamos los que Tiled resucita por defecto
            
            for datos_ene in datos["enemigos_vivos"]:
                clase_str = datos_ene["clase_enemigo"]
                
                # Factoría dinámica para saber qué clase instanciar
                if clase_str == "EsqueletoEnemigo":
                    nuevo_enemigo = EsqueletoEnemigo()
                elif clase_str == "DuendeEnemigo":
                    nuevo_enemigo = DuendeEnemigo()
                elif clase_str == "CocodriloEnemigo":
                    nuevo_enemigo = CocodriloEnemigo()
                else:
                    continue # Por seguridad si hay un tipo desconocido
                
                # Aplicamos sus constantes de posición y vida del archivo
                nuevo_enemigo.center_x = datos_ene["pos_x"]
                nuevo_enemigo.center_y = datos_ene["pos_y"]
                nuevo_enemigo.health = datos_ene["vida_actual"]
                nuevo_enemigo.cooldown = datos_ene["cooldown_actual"]
                
                # Lo añadimos a la lista viva del juego
                juego_view.enemy_list.append(nuevo_enemigo)
                
            # 6. Sincronizamos las banderas de progreso
            juego_view.jefe1_muerto = datos["jefes_derrotados"]["jefe_1"]
            
            # 7. Cambiamos la vista para empezar a jugar inmediatamente
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