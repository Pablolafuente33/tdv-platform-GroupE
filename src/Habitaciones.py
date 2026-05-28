"""
Aquí generamos las diferentes habitaciones del juego a partir de los ficheros Tiled.
En cada .tmx hay:
    - suelo (Sin colisiones)
    - pared (Colisiones al borde de las salas)
    - obstaculos (Objetos dentro de la sala donde colisionamos)
"""

import arcade
import os
from Entidades.Enemigos import EsqueletoEnemigo, DuendeEnemigo, CocodriloEnemigo
from constantes import WINDOW_HEIGHT, WINDOW_WIDTH

# ConstaNTES DE VENTANA

TILE_SIZE     = 64
WALL_COLS     = WINDOW_WIDTH  // TILE_SIZE
WALL_ROWS     = WINDOW_HEIGHT // TILE_SIZE
DOOR_TILES    = 3

#Escala para los tiles
#Ancho: 120/(15*32) = 2.6666
#Alto: 704 / (9*32) = 2.4444
TILE_SCALING = 2.5

OPUESTO = {"r":"l", "l":"r", "u":"d", "d":"u"}

#Donde se encuentran los tilemaps
MAPS_DIR = os.path.join('assets', 'maps') 
class Puerta:
    def __init__(self, side:str, leads_to: int):
        self.side = side
        self.leads_to = leads_to


"""
-------------------------------------------------------------------------------------
--------------------             CLASE       HABITACIÓN           -------------------
-------------------------------------------------------------------------------------
"""
class Habitacion:
    def __init__(self, room_id: int, puertas: list, tmx_dir:str):
        self.room_id = room_id
        self.puertas = puertas
        self.tmx_dir = tmx_dir
        self.nivel_pasado = False

        self.tile_map = None
        self.scene = None
    
    def construir_habitacion(self) -> arcade.Scene:
        """Cargamos el TileMap y devuelve una escena con las capas de la lista.
        Las paredes y los obstáculos tienen colisiones automáticamente
        Nos devolverá la escena con todos los obstáculos."""

        ruta = os.path.join(MAPS_DIR, self.tmx_dir)
        print(f'Cargando mapa: {ruta}')
        layer_options = {
            "pared":{
                "use_spatial_hash" : True
            },
            "obstaculos":{
                "use_spatial_hash" : True
            }, 
            "puertas_abiertas":{
                "use_spatial_hash" : True
            },
            "puertas_cerradas":{
                "use_spatial_hash" : True
            }
        }

        self.tile_map = arcade.load_tilemap(ruta, scaling = TILE_SCALING, layer_options= layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        return self.scene
    
    def get_wall_list(self) -> arcade.SpriteList:
        """
        Obtenemos una lista con las paredes y los obstáculos de la sala
        """
        obstaculos = arcade.SpriteList(use_spatial_hash = True)

        if self.scene :
            try:
                for s in self.scene["pared"]:
                    obstaculos.append(s)
            except KeyError:
                pass
            try:
                for s in self.scene["obstaculos"]:
                    obstaculos.append(s)
            except KeyError:
                pass
            try:
                for s in self.scene["puertas_cerradas"]:
                    obstaculos.append(s)
            except KeyError:
                pass
        return obstaculos


    def spawn(self) -> list:                                               
        """
        Devuelve lista de enemigos ya instanciados y posicionados.
        Sobreescribir en cada subclase para definir los enemigos de esa sala.
        """                                                                
        return []   
    
    # ===========================================================================
# Salas concretas — añade aquí las tuyas
# ===========================================================================
 
class Room0(Habitacion):
    """Sala inicial — habitación simple, puerta a la derecha."""
    def __init__(self):
        super().__init__(0, 
                         puertas=[Puerta("r", leads_to=1)],
                         tmx_dir="room0.tmx")


 
 
class Room1(Habitacion):
    """Segunda sala — pilares centrales, puertas izquierda y derecha."""
    def __init__(self):
        super().__init__(1, 
                         puertas =[Puerta("l",  leads_to=0),Puerta("r", leads_to=2)],
                         tmx_dir = "room1.tmx")

    
    def spawn(self) -> list:                                              
        if self.nivel_pasado:
            return []
        
        cx = (WINDOW_WIDTH)  // 2                               
        cy = (WINDOW_HEIGHT)  // 2                               
        enemigos = []                                                     
        for dx, dy in [(-200, 100), (200, -100)]:                         
            e = DuendeEnemigo()                                           
            e.center_x = cx + dx                                          
            e.center_y = cy + dy                                          
            enemigos.append(e)                                             
        return enemigos  
 
class Room2(Habitacion):
    """Tercera sala — muros internos, puertas izquierda y arriba."""
    def __init__(self):
        super().__init__(2, 
                        puertas=[Puerta("l", leads_to=1),Puerta("u",   leads_to=3)],
                        tmx_dir= "room2.tmx"
                                   )
 
    def spawn(self) -> list:                                               
        if not self.nivel_pasado:
            cx = (WINDOW_WIDTH)  // 2                               
            cy = (WINDOW_HEIGHT)  // 2                               
            enemigos = []                                                     
            for EnemyClass, dx, dy in [                                       
                (EsqueletoEnemigo, -150,  50),                                
                (EsqueletoEnemigo,     150, -50),                                
            ]:                                                                
                e = EnemyClass()                                              
                e.center_x = cx + dx                                          
                e.center_y = cy + dy                                          
                enemigos.append(e)                                             
            return enemigos
        else:
            return [] 
 
 
class Room3(Habitacion):
    def __init__(self):
        super().__init__(3, 
                         puertas=[
                             Puerta("d", leads_to=2), 
                             Puerta("u", leads_to=4) 
                         ],
                         tmx_dir="room3.tmx")

    def spawn(self) -> list:                                               
        if not self.nivel_pasado:
            cx = (WINDOW_WIDTH)  // 2                               
            cy = (WINDOW_HEIGHT) // 2                               
            e = CocodriloEnemigo()                                             
            e.center_x = cx                                                     
            e.center_y = cy                                                     
            return [e]
        else:
            return []

class Room4(Habitacion):
    def __init__(self):
        super().__init__(4, 
                         puertas=[
                             Puerta("d", leads_to=3) 
                         ],
                         tmx_dir="room4.tmx")

HABITACIONES = [Room0(), Room1(), Room2(), Room3(), Room4()]