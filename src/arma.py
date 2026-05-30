import arcade
import os
import math
from constantes import RIGHT, UP, LEFT, DOWN 


class ArmaCuerpoACuerpo(arcade.Sprite): #base para varias armas cuerpo a cuerpo 
    def __init__(self, danno , rango , cooldown, imagen, escala, nombre, dur_ataque):        
        super().__init__(imagen, escala)
        self.danno = danno
        self.rango = rango
        self.cooldown_max = cooldown
        self.nombre = nombre
        self.cooldown = 0
        self.atacar = True

        self.tiempo_visible = 0.0
        self.dur_ataque = dur_ataque
                
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
            imagen      = os.path.join('assets','objects','espada.png'),
            escala      = 0.4,
            nombre      = "Espada",
            dur_ataque  = 0.1 
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

class Lanza(ArmaCuerpoACuerpo):
    def __init__(self):
        super().__init__(
            danno       = 20, # Menos daño que la espada
            rango       = 100, # ¡Pero casi el doble de alcance!
            cooldown    = 0.8,
            imagen      = os.path.join('assets','objects','lanza.png'),
            escala      = 0.4,
            nombre      = "Lanza",
            dur_ataque  = 0.2, # Un poco más lenta
        )

    def draw_ataque(self, player_sprite):
        if self.tiempo_visible <= 0:
            return

        # Para la estocada, calculamos cuánto sale el arma (de 0 al máximo y vuelve a 0)
        # Usamos una parábola matemática sencilla con el progreso
        progreso = 1.0 - (self.tiempo_visible / self.dur_ataque)
        
        # Esto hace que el arma salga hasta el rango máximo en la mitad del tiempo y luego retroceda
        extension = math.sin(progreso * math.pi) * self.rango

        inicio_x = player_sprite.center_x
        inicio_y = player_sprite.center_y
        fin_x = inicio_x
        fin_y = inicio_y

        # Direcciones: 0 (Der), 1 (Izq), 2 (Abajo), 3 (Arriba)
        if player_sprite.facing_direction == 0:
            fin_x += extension
        elif player_sprite.facing_direction == 1:
            fin_x -= extension
        elif player_sprite.facing_direction == 2: 
            fin_y -= extension
        elif player_sprite.facing_direction == 3: 
            fin_y += extension

        # Dibujamos una línea recta hacia adelante (color marrón madera)
        arcade.draw_line(
            start_x=inicio_x, start_y=inicio_y, 
            end_x=fin_x, end_y=fin_y, 
            color=arcade.csscolor.SADDLE_BROWN, 
            line_width=6 # Más fina que la espada
        )
        """
        arcade.draw_triangle_filled(

        )"""

    def calcular_impactos(self, enemy_list, player_sprite):
        for enemy in enemy_list:
            dx = enemy.center_x - player_sprite.center_x
            dy = enemy.center_y - player_sprite.center_y
            distancia_real = math.sqrt(dx**2 + dy**2)
            distancia_al_borde = distancia_real - (enemy.width / 2)
            
            if distancia_al_borde <= self.rango:
                # Para la lanza, el margen de desalineación es muchísimo menor (es un ataque muy estrecho)
                margen_lateral = 15 
                
                # Comprobamos que esté en la dirección correcta y bien alineado
                if player_sprite.facing_direction == 0 and dx > 0 and abs(dy) < margen_lateral:
                    enemy.recibir_danno(self.danno)
                elif player_sprite.facing_direction == 1 and dx < 0 and abs(dy) < margen_lateral:
                    enemy.recibir_danno(self.danno)
                elif player_sprite.facing_direction == 2 and dy < 0 and abs(dx) < margen_lateral:
                    enemy.recibir_danno(self.danno)
                elif player_sprite.facing_direction == 3 and dy > 0 and abs(dx) < margen_lateral:
                    enemy.recibir_danno(self.danno)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Esto es lo que se va a ver que va a ir viajando por la pantalla

class Proyectil(arcade.Sprite): 
    def __init__(self, velocidad, rango, danno, imagen, escala):
        # OJO: Eliminado el 'self' de dentro del super().__init__
        super().__init__(imagen, escala)
        self.velocidad = velocidad
        self.rango = rango
        self.danno = danno

        self.inicio_x = None
        self.inicio_y = None
    def getDanno(self):
        return self.danno

    def update(self, delta_time):
        #PAra saber luego cuanto se ha movido
        if self.inicio_x is None:
            self.inicio_x = self.center_x
            self.inicio_y = self.center_y
        
        # Movemos la flecha sumando su velocidad
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        # Calculamos cuánto ha avanzado
        avance = math.sqrt((self.center_x - self.inicio_x)**2 + (self.center_y - self.inicio_y)**2)
        # Si supera su rango máximo de vuelo, se elimina a sí misma
        if avance >= self.rango:
            self.kill()

class Flecha(Proyectil):
    def __init__(self, start_x, start_y, direccion):
        super().__init__(
            velocidad = 10, 
            rango     = 400, 
            danno     = 15, 
            imagen    = os.path.join('assets','objects','lanza.png'), # Asegúrate de tener este PNG
            escala    = 0.1
        )
        self.center_x = start_x
        self.center_y = start_y

        # Direcciones: 0 (Der), 1 (Izq), 2 (Abajo), 3 (Arriba)dw
        if direccion == 0:
            self.change_x = self.velocidad
            self.angle = 0
        elif direccion == 1:
            self.change_x = -self.velocidad
            self.angle = 180
        elif direccion == 2:
            self.change_y = -self.velocidad
            self.angle = 270
        elif direccion == 3:
            self.change_y = self.velocidad
            self.angle = 90

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Esto es lo que va a lanzar el proyectil
class ArmaDistancia(arcade.Sprite): 
    def __init__(self, cooldown, imagen, escala, nombre):
        super().__init__(imagen, escala)
        self.cooldown_max = cooldown
        self.cooldown = 0
        self.atacar = True
        self.nombre = nombre

    def on_update(self, delta_time, player_sprite = None):
        if self.cooldown > 0:
            self.cooldown -= delta_time 
            self.atacar = False
        if self.cooldown <= 0:
            self.cooldown = 0
            self.atacar = True

    # Para disparar, devolveremos el objeto Proyectil creado
    def use(self, enemy_list, player_sprite):
        if self.atacar:
            self.atacar = False
            self.cooldown = self.cooldown_max
            return self.disparar(player_sprite)
        return None
        
    def disparar(self, player_sprite):
        pass # A definir por cada arma hija

    def draw_ataque(self, player_sprite):
        pass

class Arco(ArmaDistancia):
    def __init__(self):
        super().__init__(
            cooldown = 1.0, 
            imagen   = os.path.join('assets','objects','lanza.png'), 
            escala   = 0.4,
            nombre   = "Arco"
        )

    def disparar(self, player_sprite):
        # Creamos una flecha en la posición del jugador apuntando hacia donde mira
        nueva_flecha = Flecha(
            start_x = player_sprite.center_x,
            start_y = player_sprite.center_y,
            direccion = player_sprite.facing_direction
        )
        return nueva_flecha
    
class PocionCuración(arcade.Sprite):
    def __init__(self):
        imagen = os.path.join('assets', 'objects', 'pocion_vida.png')
        super().__init__(imagen, scale = 1.5)
        self.curación = 50
