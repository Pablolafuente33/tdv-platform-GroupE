"""
Aqui se generarán las habitaciones diferentes de nuestro mapa.
- En cada habitación habrá una lista de puertas.
- Debemos de crear una función que construya la sala, cada una será construida
de forma diferente porque no todas vana a tener las  mismas puertas.
- A partir de aquí se deberá de spawnear los enemigos. 
"""

import arcade
from enemigos import EsqueletoEnemigo, DuendeEnemigo, CocodriloEnemigo

# ConstaNTES DE VENTANA
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

TILE_SIZE     = 64
WALL_COLS     = WINDOW_WIDTH  // TILE_SIZE
WALL_ROWS     = WINDOW_HEIGHT // TILE_SIZE
DOOR_TILES    = 3

OPUESTO = {"r":"l", "l":"r", "u":"d", "d":"u"}

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
    def __init__(self, room_id: int, puertas: list):
        self.room_id = room_id
        self.puertas = puertas
    
    def construir_habitacion(self, wall_list:arcade.SpriteList):
        """Construimos las paredes exteriores de las habitaciones"""
        door_tiles = self.door_tile_indices()
        for col in range (WALL_COLS):
            for row in range (WALL_ROWS):
                is_border = (col == 0 or col == WALL_COLS - 1 or 
                             row == 0 or row == WALL_ROWS - 1)
                if not is_border or (col, row) in door_tiles:
                    continue
                self.añadir_pared(wall_list, col, row)
    
    def door_tile_indices(self) -> set:
        half  = DOOR_TILES // 2
        tiles = set()
        for door in self.puertas:
            if door.side == "r":
                col, cr = WALL_COLS - 1, WALL_ROWS // 2
                for dr in range(-half, half + 1):
                    tiles.add((col, cr + dr))
            elif door.side == "l":
                col, cr = 0, WALL_ROWS // 2
                for dr in range(-half, half + 1):
                    tiles.add((col, cr + dr))
            elif door.side == "u":
                row, cc = WALL_ROWS - 1, WALL_COLS // 2
                for dc in range(-half, half + 1):
                    tiles.add((cc + dc, row))
            elif door.side == "d":
                row, cc = 0, WALL_COLS // 2
                for dc in range(-half, half + 1):
                    tiles.add((cc + dc, row))
        return tiles
    
    @staticmethod
    def añadir_pared(wall_list, col, row, color=(60, 60, 60)):
        wall = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE, color)
        wall.center_x = col * TILE_SIZE + TILE_SIZE // 2
        wall.center_y = row * TILE_SIZE + TILE_SIZE // 2
        wall_list.append(wall)
 
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
        super().__init__(0, puertas=[Puerta("r", leads_to=1)])


 
 
class Room1(Habitacion):
    """Segunda sala — pilares centrales, puertas izquierda y derecha."""
    def __init__(self):
        super().__init__(1, puertas=[Puerta("l",  leads_to=0),
                                   Puerta("r", leads_to=2)])
 
    def construir_habitacion(self, wall_list):
        super().construir_habitacion(wall_list)
        # Dos pilares de 2×2 tiles en el centro
        for col, row in [(6,3),(6,4),(7,3),(7,4),(13,3),(13,4),(14,3),(14,4)]:
            self.añadir_pared(wall_list, col, row, color=(80, 60, 40))
    
    def spawn(self) -> list:                                              
        cx = (ROOM_LEFT + ROOM_RIGHT)  // 2                               
        cy = (ROOM_BOTTOM + ROOM_TOP)  // 2                               
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
        super().__init__(2, puertas=[Puerta("l", leads_to=1),
                                   Puerta("u",   leads_to=3)])
 
    def construir_habitacion(self, wall_list):
        super().construir_habitacion(wall_list)
        for col in range(2, 9):
            self.añadir_pared(wall_list, col, 3, color=(70, 50, 30))
        for col in range(11, 18):
            self.añadir_pared(wall_list, col, 7, color=(70, 50, 30))

    def spawn(self) -> list:                                               
        cx = (WINDOW_WIDTH)  // 2                               
        cy = (WINDOW_HEIGHT)  // 2                               
        enemigos = []                                                     
        for EnemyClass, dx, dy in [                                       
            (EsqueletoEnemigo, -150,  50),                                
            (DuendeEnemigo,     150, -50),                                
        ]:                                                                
            e = EnemyClass()                                              
            e.center_x = cx + dx                                          
            e.center_y = cy + dy                                          
            enemigos.append(e)                                             
        return enemigos 
 
 
class Room3(Habitacion):
    """Sala final — despejada, puerta abajo."""
    def __init__(self):
        super().__init__(3, puertas =[Puerta("d", leads_to=2)])
    def spawn(self) -> list:                                               # NUEVO
        cx = (ROOM_LEFT + ROOM_RIGHT)  // 2                               # NUEVO
        cy = (ROOM_BOTTOM + ROOM_TOP)  // 2                               # NUEVO
        e = CocodriloEnemigo()                                             # NUEVO
        e.center_x = cx                                                    # NUEVO
        e.center_y = cy                                                    # NUEVO
        return [e]
 
 
HABITACIONES = [Room0(), Room1(), Room2(), Room3()]