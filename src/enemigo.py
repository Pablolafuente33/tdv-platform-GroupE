import math
import arcade
from personajes import Character

# Constantes de dirección
RIGHT_FACING = 0
LEFT_FACING = 1
UP_FACING = 2
DOWN_FACING = 3

class Enemigo(Character):
    def __init__(self, nombre_carpeta, nombre_archivo):
        super().__init__(nombre_carpeta, nombre_archivo)
        self.velocidad = 0
        self.health = 0
        self.should_update_walk = 0
        self.detect_distance = 250

    def update_animation(self, delta_time: float):
        # 1. Determinar la dirección
        if self.change_x < 0:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0:
            self.facing_direction = RIGHT_FACING
        elif self.change_y > 0:
            self.facing_direction = UP_FACING
        elif self.change_y < 0:
            self.facing_direction = DOWN_FACING

        # Si el enemigo está quieto
        if self.change_x == 0 and self.change_y == 0:
            if self.facing_direction in [UP_FACING, DOWN_FACING]:
                self.texture = self.idle_texture_pair[0]
            else:
                self.texture = self.idle_texture_pair[self.facing_direction]
            return

        self.should_update_walk += 1
        if self.should_update_walk > 5:
            self.cur_texture += 1
            
            if self.cur_texture > 7: 
                    self.cur_texture = 0
                    
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0

    def seguir_jugador(self, jugador):
        
        # Calcular la distancia entre el enemigo y el jugador
        distance = math.sqrt((jugador.center_x - self.center_x)**2 + (jugador.center_y - self.center_y)**2)
        
        if distance < self.detect_distance:
            
            distancia_x = jugador.center_x - self.center_x
            distancia_y = jugador.center_y - self.center_y
            angulo = math.atan2(distancia_y, distancia_x)
            
            self.change_x = math.cos(angulo) * self.velocidad
            self.change_y = math.sin(angulo) * self.velocidad
        
        else:
            self.change_x = 0
            self.change_y = 0

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

class EsqueletoEnemigo(Enemigo):
    def __init__(self):
        super().__init__("skeleton", "skeleton")
        self.health = 100
        self.velocidad = 2
        self.detect_distance = 300
        
class DuendeEnemigo(Enemigo):
    def __init__(self):
        super().__init__("goblin", "goblin")
        self.health = 50
        self.velocidad = 3
        self.detect_distance = 250
        
class CocodriloEnemigo(Enemigo):
    def __init__(self):
        super().__init__("crocodile", "crocodile")
        self.health = 150
        self.velocidad = 1.5
        self.detect_distance = 100