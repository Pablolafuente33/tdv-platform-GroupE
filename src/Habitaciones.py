"""
Aquí generamos las diferentes habitaciones del juego a partir de los ficheros Tiled.
En cada .tmx hay:
    - suelo (Sin colisiones)
    - pared (Colisiones al borde de las salas)
    - obstaculos (Objetos dentro de la sala donde colisionamos)
"""

import arcade
import os
import random
import math
from Entidades.enemigos import Enemigo1, Enemigo2, Enemigo3, Boss1, Boss2, Boss3
from constantes import WINDOW_HEIGHT, WINDOW_WIDTH

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


    def spawn(self, dificultad: str, jugador) -> list:                                               
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

    
    def spawn(self, dificultad: str, jugador) -> list:                                              
        if self.nivel_pasado:
            return []
        
        match dificultad:
            case "Facil":
                cantidad_enemigos = 2
            case "Normal":
                cantidad_enemigos = 3
            case "Dificil":
                cantidad_enemigos = 4
            case _ : cantidad_enemigos = 3

        enemigos = []     

        # Miramos los obstáculos de la habitación
        lista_obstaculos = self.get_wall_list()

        margen = 80
        RADIO = 2500 if dificultad != "Dificil" else 0

        for _ in range(cantidad_enemigos):
            e = Enemigo2()
            intentos = 0
            posicion_valida = False

            while not posicion_valida and intentos < 100:
                intentos += 1
                #Tomamos una posición aleatoria
                e.center_x = random.randint(margen,WINDOW_WIDTH - margen)                                                
                e.center_y = random.randint(margen,WINDOW_HEIGHT - margen)

                # Ci¡omprobamos que no spawnee encima del jugador
                distancia_al_jugador = math.sqrt(
                    (e.center_x - jugador.center_x) ** 2 + 
                    (e.center_y - jugador.center_y) ** 2
                )
                # Si está demasiado cerca, forzamos repetir el bucle sin comprobar colisiones
                if distancia_al_jugador < RADIO:
                    continue
                
                #Comprobamos que no se choqye con un obstáculo
                colision_obst = arcade.check_for_collision_with_list(e, lista_obstaculos)                                                
                colisiona_enemigo = arcade.check_for_collision_with_list(e, arcade.SpriteList(use_spatial_hash=False))
                for enemigo_colocado in enemigos:
                    if arcade.check_for_collision(e, enemigo_colocado):
                        colisiona_con_otro_enemigo = True
                
                # Si no choca con nada, la posición es apta
                if not colision_obst and not colisiona_con_otro_enemigo:
                    posicion_valida = True

            #Lo añadimos a la lista
            enemigos.append(e)
        return enemigos
 
class Room2(Habitacion):
    """Tercera sala — muros internos, puertas izquierda y arriba."""
    def __init__(self):
        super().__init__(2, 
                        puertas=[Puerta("l", leads_to=1),Puerta("u",   leads_to=3)],
                        tmx_dir= "room2.tmx"
                                   )
 
    def spawn(self, dificultad:str, jugador) -> list:                                               
        if not self.nivel_pasado:
            cx = (WINDOW_WIDTH)  // 2                               
            cy = (WINDOW_HEIGHT) // 2                               
            e = Boss1(dificultad)                                             
            e.center_x = cx                                                     
            e.center_y = cy                                                     
            return [e]
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

    def spawn(self, dificultad: str, jugador) -> list:
        if self.nivel_pasado:
            return []
        
        match dificultad:
            case "Facil":
                cantidad_enemigos = 1
            case "Normal":
                cantidad_enemigos = 2
            case "Dificil":
                cantidad_enemigos = 3
            case _ : 
                cantidad_enemigos = 2

        enemigos = []     

        # Miramos los obstáculos de la habitación
        lista_obstaculos = self.get_wall_list()

        margen = 80
        RADIO = 2500 if dificultad != "Dificil" else 0

        for _ in range(cantidad_enemigos):
            e = Enemigo1()
            intentos = 0
            posicion_valida = False

            while not posicion_valida and intentos < 100:
                intentos +=1
                #Tomamos una posición aleatoria
                e.center_x = random.randint(margen,WINDOW_WIDTH - margen)                                                
                e.center_y = random.randint(margen,WINDOW_HEIGHT - margen)

                # Ci¡omprobamos que no spawnee encima del jugador
                distancia_al_jugador = math.sqrt(
                    (e.center_x - jugador.center_x) ** 2 + 
                    (e.center_y - jugador.center_y) ** 2
                )
                # Si está demasiado cerca, forzamos repetir el bucle sin comprobar colisiones
                if distancia_al_jugador < RADIO:
                    continue
                
                #Comprobamos que no se choqye con un obstáculo
                colision_obst = arcade.check_for_collision_with_list(e, lista_obstaculos)                                                
                colisiona_enemigo = arcade.check_for_collision_with_list(e, arcade.SpriteList(use_spatial_hash=False))
                for enemigo_colocado in enemigos:
                    if arcade.check_for_collision(e, enemigo_colocado):
                        colisiona_con_otro_enemigo = True
                
                # Si no choca con nada, la posición es apta
                if not colision_obst and not colisiona_con_otro_enemigo:
                    posicion_valida = True

            #Lo añadimos a la lista
            enemigos.append(e)
        return enemigos                                               

class Room4(Habitacion):
    def __init__(self):
        super().__init__(4, 
                         puertas=[
                             Puerta("d", leads_to=3),
                             Puerta("l", leads_to=5),
                             Puerta("r", leads_to=6) 
                         ],
                         tmx_dir="room4.tmx")
        
    def spawn(self, dificultad:str, jugador) -> list:                                               
        if self.nivel_pasado:
            return []
        
        match dificultad:
            case "Facil":
                cantidad_enemigos = 1
            case "Normal":
                cantidad_enemigos = 2
            case "Dificil":
                cantidad_enemigos = 4
            case _ : cantidad_enemigos = 3

        enemigos = []     

        # Miramos los obstáculos de la habitación
        lista_obstaculos = self.get_wall_list()

        margen = 80
        RADIO = 2500 if dificultad != "Dificil" else 0

        for _ in range(cantidad_enemigos):
            e = Enemigo3()
            intentos = 0
            posicion_valida = False

            while not posicion_valida and intentos < 100:
                intentos += 1
                #Tomamos una posición aleatoria
                e.center_x = random.randint(margen,WINDOW_WIDTH - margen)                                                
                e.center_y = random.randint(margen,WINDOW_HEIGHT - margen)

                # Ci¡omprobamos que no spawnee encima del jugador
                distancia_al_jugador = math.sqrt(
                    (e.center_x - jugador.center_x) ** 2 + 
                    (e.center_y - jugador.center_y) ** 2
                )
                # Si está demasiado cerca, forzamos repetir el bucle sin comprobar colisiones
                if distancia_al_jugador < RADIO:
                    continue
                
                #Comprobamos que no se choqye con un obstáculo
                colision_obst = arcade.check_for_collision_with_list(e, lista_obstaculos)                                                
                colisiona_enemigo = arcade.check_for_collision_with_list(e, arcade.SpriteList(use_spatial_hash=False))
                for enemigo_colocado in enemigos:
                    if arcade.check_for_collision(e, enemigo_colocado):
                        colisiona_con_otro_enemigo = True
                
                # Si no choca con nada, la posición es apta
                if not colision_obst and not colisiona_con_otro_enemigo:
                    posicion_valida = True

            #Lo añadimos a la lista
            enemigos.append(e)
        return enemigos
        
class Room5(Habitacion):
    def __init__(self):
        super().__init__(5, 
                         puertas=[
                             Puerta("r", leads_to=4),
                             Puerta("u", leads_to=7) 
                         ],
                         tmx_dir="room5.tmx")
    def spawn(self, dificultad:str, jugador) -> list:                                               
        if not self.nivel_pasado:
            cx = (WINDOW_WIDTH)  // 2                               
            cy = (WINDOW_HEIGHT)  // 2                               
            enemigos = []                                                     
            for EnemyClass, dx, dy in [                                       
                (Enemigo1, -150,  100),
                (Enemigo2, 100, 100)                                ,                                
            ]:                                                                
                e = EnemyClass()                                              
                e.center_x = cx + dx                                          
                e.center_y = cy + dy                                          
                enemigos.append(e)                                             
            return enemigos
        else:
            return []
         
class Room6(Habitacion):
    def __init__(self):
        super().__init__(6, 
                         puertas=[
                             Puerta("l", leads_to=4)
                         ],
                         tmx_dir="room6.tmx")
                                                   
    def spawn(self, dificultad:str, jugador) -> list:                                               
        if not self.nivel_pasado:
            cx = (WINDOW_WIDTH)  // 2                               
            cy = (WINDOW_HEIGHT) // 2                               
            e = Boss2(dificultad)                                             
            e.center_x = cx                                                     
            e.center_y = cy                                                     
            return [e]
        else:
            return []
        
class Room7(Habitacion):
    def __init__(self):
        super().__init__(7, 
                         puertas=[
                             Puerta("d", leads_to=5)
                         ],
                         tmx_dir="room7.tmx")
    def spawn(self, dificultad:str, jugador) -> list:                                               
        if not self.nivel_pasado:
            cx = (WINDOW_WIDTH)  // 2                               
            cy = (WINDOW_HEIGHT) // 2                               
            e = Boss3(dificultad)                                             
            e.center_x = cx                                                     
            e.center_y = cy                                                     
            return [e]
        else:
            return []
    
        
HABITACIONES = [Room0(), Room1(), Room2(), Room3(), Room4(), Room5(), Room6(), Room7()]