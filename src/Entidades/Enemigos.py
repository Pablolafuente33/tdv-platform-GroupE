import math

import random

from pathlib import Path
from Entidades.gestor_animaciones import Gestor_animaciones
import os
import arcade

from arma import Espada 

# Constants used to track the direction a character is facing
RIGHT_FACING = 0
LEFT_FACING = 1
UP_FACING = 2
DOWN_FACING = 3


"""
=============================================================================================================================
===========================================      ENEMIGOS       =============================================================
=============================================================================================================================
"""

class Enemigo(arcade.TextureAnimationSprite):
    def __init__(self):
        super().__init__()
        self.velocidad = 0
        self.health = 0
        self.max_health = 0
        self.detect_distance = 250
        self.vivo = True
        self.cambio_direccion_timer = 0
        self.intervalo_cambio = 1.5

        self.danno = 0
        self.coolldown_max = 0
        self.cooldown = 0

    

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

        
            
    def caminar_aleatorio(self, delta_time):
        self.cambio_direccion_timer += delta_time
        
        if self.cambio_direccion_timer >= self.intervalo_cambio:
            opcion = random.randint(0, 4) 
            
            if opcion == 0:
                self.change_x, self.change_y = 0, 0
            elif opcion == 1:
                self.change_x, self.change_y = 0, self.velocidad
            elif opcion == 2:
                self.change_x, self.change_y = 0, -self.velocidad
            elif opcion == 3:
                self.change_x, self.change_y = -self.velocidad, 0
            elif opcion == 4:
                self.change_x, self.change_y = self.velocidad, 0
                
            self.cambio_direccion_timer = 0 

        self.update_animation_state(delta_time)

    def recibir_danno(self, cantidad):

        #Aquí deberia de azctualizrse, comprobar si hay colisión ocn otro sprite de una arma
        self.health -= cantidad
        if self.health <= 0:
            self.health = 0
            self.remove_from_sprite_lists()

    def update(self,delta_time):
        if self.cooldown > 0:
            self.cooldown -= delta_time

        self.caminar_aleatorio(delta_time)

        self.update_animation_state(delta_time)

    def atacar_jugador (self, jugador):
        if self.cooldown <= 0:
            jugador.health -= self.danno
            self.cooldown = self.coolldown_max
            print(f'Enemigo ataca !! Vida jugador {jugador.health}')

    def update_animation_state(self,delta_time):
        pass
class EsqueletoEnemigo(Enemigo):
    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.velocidad = 2
        self.detect_distance = 300

        self.danno = 10
        self.coolldown_max = 10
        self.cooldown = 0

        self.scale = 2.5

        #Se inicia gestor de animaciones, dando los valores generales del spritesheet para hacer las animaciones
        self.gestor_animaciones = Gestor_animaciones(
            sprite=self,
            spritesheet_path = os.path.join('assets','graphics','Enemigo_1Spritesheet.png'),
            tamanno_sprite= (64, 64),
            columns= 6,
            count=6,
            duracion= 150
        )


    def update_animation_state(self, delta_time):
        self.gestor_animaciones.update(self.change_x, self.change_y, delta_time)
        
class DuendeEnemigo(Enemigo):
    def __init__(self):
        super().__init__()
        self.health = 50
        self.max_health = 50
        self.velocidad = 3
        self.detect_distance = 250
        
        self.danno = 25
        self.coolldown_max = 7
        self.cooldown = 0

        self.scale = 2.5

        #Se inicia gestor de animaciones, dando los valores generales del spritesheet para hacer las animaciones
        self.gestor_animaciones = Gestor_animaciones(
            sprite=self,
            spritesheet_path = os.path.join('assets','graphics','Enemigo_2.png'),
            tamanno_sprite= (64, 64),
            columns= 6,
            count=6,
            duracion= 150
        )

    
    def update_animation_state(self, delta_time):
        self.gestor_animaciones.update(self.change_x, self.change_y, delta_time)


class CocodriloEnemigo(Enemigo):
    def __init__(self):
        super().__init__()
        self.health = 150
        self.max_health = 150
        self.velocidad = 1.5
        self.detect_distance = 100  

        self.danno = 5
        self.coolldown_max = 2
        self.cooldown = 0

        self.scale = 2.5


        #Se inicia gestor de animaciones, dando los valores generales del spritesheet para hacer las animaciones
        self.gestor_animaciones = Gestor_animaciones(
            sprite=self,
            spritesheet_path = os.path.join('assets','graphics','Boss_1.png'),
            tamanno_sprite= (64, 64),
            columns= 6,
            count=6,
            duracion= 150
        )


    def update_animation_state(self, delta_time):
        self.gestor_animaciones.update(self.change_x, self.change_y, delta_time)
