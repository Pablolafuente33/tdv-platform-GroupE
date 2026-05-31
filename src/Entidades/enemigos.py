import math

import random

from pathlib import Path
from entidades.gestor_animaciones import Gestor_animaciones
import os
import arcade

 

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
class Enemigo1(Enemigo):
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
            spritesheet_idle_path = os.path.join('assets','graphics','Enemigo_1Spritesheet.png'),
            tamanno_sprite= (64, 64),
            columns= 6,
            count=6,
            duracion= 150
        )


    def update_animation_state(self, delta_time):
        self.gestor_animaciones.update(self.change_x, self.change_y, delta_time)
        
class Enemigo2(Enemigo):
    def __init__(self):
        super().__init__()
        self.health = 50
        self.max_health = 50
        self.velocidad = 3
        self.detect_distance = 250
        
        self.danno = 15
        self.coolldown_max = 7
        self.cooldown = 0

        self.scale = 2.5

        #Se inicia gestor de animaciones, dando los valores generales del spritesheet para hacer las animaciones
        self.gestor_animaciones = Gestor_animaciones(
            sprite=self,
            spritesheet_idle_path = os.path.join('assets','graphics','Enemigo_2.png'),
            tamanno_sprite= (64, 64),
            columns= 6,
            count=6,
            duracion= 150
        )

    
    def update_animation_state(self, delta_time):
        self.gestor_animaciones.update(self.change_x, self.change_y, delta_time)

class Enemigo3(Enemigo):
    def __init__(self):
        super().__init__()
        self.health = 40
        self.max_health = 40
        self.velocidad = 3
        self.detect_distance = 250
        
        self.danno = 15
        self.coolldown_max = 5
        self.cooldown = 0

        self.scale = 2.5

        #Se inicia gestor de animaciones, dando los valores generales del spritesheet para hacer las animaciones
        self.gestor_animaciones = Gestor_animaciones(
            sprite=self,
            spritesheet_idle_path = os.path.join('assets','graphics','Enemigo_3.png'),
            tamanno_sprite= (64, 64),
            columns= 6,
            count=6,
            duracion= 150
        )

    
    def update_animation_state(self, delta_time):
        self.gestor_animaciones.update(self.change_x, self.change_y, delta_time)


class Boss1(Enemigo):
    def __init__(self, dificultad: str):
        super().__init__()
        
        match dificultad:
            case "Facil":
                self.max_health = 100
                self.velocidad = 1.1
                self.detect_distance = 100  
                self.danno = 10
                self.coolldown_max = 2.2
            case "Normal":
                self.max_health = 125
                self.velocidad = 1.5
                self.detect_distance = 100  
                self.danno = 12
                self.coolldown_max = 2.1
            case "Dificil":
                self.max_health = 150
                self.velocidad = 1.6
                self.detect_distance = 200  
                self.danno = 15
                self.coolldown_max = 2
            case _:
                self.max_health = 150
                self.velocidad = 1.5
                self.detect_distance = 100  
                self.danno = 12
                self.coolldown_max = 2.1
        
        self.health = self.max_health
        self.cooldown = 0
        self.scale = 2.5


        #Se inicia gestor de animaciones, dando los valores generales del spritesheet para hacer las animaciones
        self.gestor_animaciones = Gestor_animaciones(
            sprite=self,
            spritesheet_idle_path = os.path.join('assets','graphics','Boss_1.png'),
            tamanno_sprite= (64, 64),
            columns= 6,
            count=6,
            duracion= 250
        )


    def update_animation_state(self, delta_time):
        self.gestor_animaciones.update(self.change_x, self.change_y, delta_time)

class Boss2(Enemigo):
    def __init__(self, dificultad):
        super().__init__()
        match dificultad:
            case "Facil":
                self.max_health = 250
                self.velocidad = 2
                self.detect_distance = 150  
                self.danno = 13
                self.coolldown_max = 2.5
            case "Normal":
                self.max_health = 300
                self.velocidad = 2.5
                self.detect_distance = 200  
                self.danno = 17
                self.coolldown_max = 2
            case "Dificil":
                self.max_health = 325
                self.velocidad = 1.6
                self.detect_distance = 250  
                self.danno = 21
                self.coolldown_max = 2
            case _:
                self.max_health = 300
                self.velocidad = 2.5
                self.detect_distance = 200 
                self.danno = 17
                self.coolldown_max = 2
        
        self.health = self.max_health
        self.cooldown = 0
        self.scale = 2.5


        #Se inicia gestor de animaciones, dando los valores generales del spritesheet para hacer las animaciones
        self.gestor_animaciones = Gestor_animaciones(
            sprite=self,
            spritesheet_idle_path = os.path.join('assets','graphics','Boss_2.png'),
            tamanno_sprite= (64, 64),
            columns= 6,
            count=6,
            duracion= 200
        )


    def update_animation_state(self, delta_time):
        self.gestor_animaciones.update(self.change_x, self.change_y, delta_time)

class Boss3(Enemigo):
    def __init__(self, dificultad):
        super().__init__()
        match dificultad:
            case "Facil":
                self.max_health = 400
                self.velocidad = 2.4
                self.detect_distance = 150  
                self.danno = 15
                self.coolldown_max = 2.2
            case "Normal":
                self.max_health = 450
                self.velocidad = 2.8
                self.detect_distance = 200  
                self.danno = 20
                self.coolldown_max = 2.1
            case "Dificil":
                self.max_health = 490
                self.velocidad = 3
                self.detect_distance = 2500  
                self.danno = 23
                self.coolldown_max = 1.9
            case _:
                self.max_health = 450
                self.velocidad = 2.8
                self.detect_distance = 200  
                self.danno = 20
                self.coolldown_max = 2.1
        
        self.health = self.max_health
        self.cooldown = 0
        self.scale = 2.5

        #Se inicia gestor de animaciones, dando los valores generales del spritesheet para hacer las animaciones
        self.gestor_animaciones = Gestor_animaciones(
            sprite=self,
            spritesheet_idle_path = os.path.join('assets','graphics','Boss_3.png'),
            tamanno_sprite= (64, 64),
            columns= 6,
            count=6,
            duracion= 200
        )


    def update_animation_state(self, delta_time):
        self.gestor_animaciones.update(self.change_x, self.change_y, delta_time)
