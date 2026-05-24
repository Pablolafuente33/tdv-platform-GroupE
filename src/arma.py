import arcade
import os
import math
from constantes import RIGHT, UP, LEFT, DOWN 


class ArmaCuerpoACuerpo(arcade.Sprite): #base para varias armas cuerpo a cuerpo 
    def __init__(self, danno , rango , cooldown, imagen, escala, nombre):        
        super().__init__(imagen, escala)
        self.danno = danno
        self.rango = rango
        self.cooldown_max = cooldown
        self.nombre = nombre
        self.cooldown = 0
        self.atacar = True

        self.tiempo_visible = 0.0
        self.dur_ataque = 0.1
                
    def getDanno(self):
        return self.danno

    def on_update(self, delta_time, player_sprite):
        if self.cooldown > 0:
            self.cooldown -= delta_time
            self.atacar = False
        if self.cooldown <= 0:
            self.atacar = True
            
        # Reducir el tiempo visual y hacer que el arma "siga" al jugador mientras ataca
        if self.tiempo_visible > 0:
            self.tiempo_visible -= delta_time


    def use(self, enemy_list, player_sprite):
        if self.atacar:
            # Colocamos el arma y activamos su temporizador visual
            self.tiempo_visible = self.dur_ataque
            
            self.calcular_impactos(enemy_list, player_sprite)

            self.draw_ataque(player_sprite)

            self.atacar = False 
            self.cooldown = self.cooldown_max
    
    def draw_ataque(self, player_sprite):
        pass
    
    def calcular_impactos(self, enemy_list, player_sprite):
        pass


class Espada(ArmaCuerpoACuerpo):     
    def __init__(self):
        super().__init__(
            danno       = 30,
            rango       = 60,
            cooldown    = 1,
            imagen      = os.path.join('assets','espada.png'),
            escala      = 0.4,
            nombre      = "Espada",
        )

    def calcular_impactos(self, enemy_list, player_sprite):
        for enemy in enemy_list:
            # 1. Distancia de centro a centro
            dx = enemy.center_x - player_sprite.center_x
            dy = enemy.center_y - player_sprite.center_y
            distancia_real = math.sqrt(dx**2 + dy**2)
            
            # Restamos la mitad del ancho del enemigo a la distancia
            # Así detectamos si la espada le roza el borde del sprite
            radio_enemigo = enemy.width / 2
            distancia_al_borde = distancia_real - radio_enemigo
            
            # Usamos la distancia corregida
            if distancia_al_borde <= self.rango:
                
                # He puesto un pequeño margen (dx > -10) en vez de (dx > 0) por si el enemigo está desalineado 
                margen = -15
                
                if player_sprite.facing_direction == 0 and dx > margen:   # Derecha
                    enemy.recibir_danno(self.danno)
                elif player_sprite.facing_direction == 1 and dx < -margen:# Izquierda
                    enemy.recibir_danno(self.danno)
                elif player_sprite.facing_direction == 3 and dy > margen: # Arriba 
                    enemy.recibir_danno(self.danno)
                elif player_sprite.facing_direction == 2 and dy < -margen:# Abajo 
                    enemy.recibir_danno(self.danno)

    def draw_ataque(self, player_sprite):
        """ Dibuujo de la estela de la espada
        """

        if self.tiempo_visible <= 0:
            return

        progreso = 1.0 - (self.tiempo_visible / self.dur_ataque)
        
        if player_sprite.facing_direction == 0:
            angulo_actual = 60 - (120 * progreso) 
        elif player_sprite.facing_direction == 1:
            angulo_actual = 120 + (120 * progreso)
        elif player_sprite.facing_direction == 2: 
            angulo_actual = -30 - (120 * progreso)
        elif player_sprite.facing_direction == 3: 
            angulo_actual = 150 - (120 * progreso)
        

        rad = math.radians(angulo_actual)
        
        # Punto A: La empuñadura (el centro del jugador)
        inicio_x = player_sprite.center_x
        inicio_y = player_sprite.center_y
        
        # Punto B: La punta de la espada (calculada con el ángulo y el rango)
        fin_x = inicio_x + math.cos(rad) * self.rango
        fin_y = inicio_y + math.sin(rad) * self.rango
        
        # Dibujamos una línea con grosor de 12 píxeles
        arcade.draw_line(
            start_x=inicio_x, 
            start_y=inicio_y, 
            end_x=fin_x, 
            end_y=fin_y, 
            color=arcade.csscolor.GRAY, 
            line_width=10
        )


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Esto es lo que se va a ver que va a ir viajando por la pantalla

class Proyectil(arcade.Sprite): #base para proyectiles de armas a distancia

    def __init__(self, velocidad, rango, danno, imagen, escala):
        super().__init__(self, imagen, escala)
    def getDanno(self):
        return self.danno

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Esto es lo que va a lanzar el proyectil
class ArmaDistancia(arcade.Sprite): #base para varias armas a distancia 

    def __init__(self, imagen, escala, cooldown):
        super().__init__(self, imagen, escala)

    def on_update(self, delta_time):
        if self.cooldown > 0:
            self.cooldown -= delta_time 
            self.atacar = False

        if self.cooldown <= 0:
            self.cooldown = 0
            self.atacar = True

    def getCooldown(self):
        return self.atacar
    
