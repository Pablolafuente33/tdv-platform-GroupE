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
            
        if self.tiempo_visible > 0:
            self.tiempo_visible -= delta_time

    def use(self, enemy_list, player_sprite):
        if self.atacar:
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
            danno      = 10,
            rango      = 60,
            cooldown   = 0.6,
            imagen     = os.path.join('assets', 'objects', 'lanza.png'),  # icono HUD temporal
            escala     = 0.4,
            nombre     = "Espada",
            dur_ataque = 0.5
        )
        # Icono HUD: primer frame del spritesheet
        sheet = arcade.load_spritesheet(os.path.join('assets', 'graphics', 'Espada.png'))
        frames = sheet.get_texture_grid(size=(64, 64), columns=9, count=36)
        self.texture = frames[0]

    def use(self, enemy_list, player_sprite):
        if self.atacar:
            self.atacar = False
            self.cooldown = self.cooldown_max
            from espadaAtaque import EspadaAtaque  # ← e minúscula
            return EspadaAtaque(
                x          = player_sprite.center_x,
                y          = player_sprite.center_y,
                direccion  = player_sprite.facing_direction,
                enemy_list = enemy_list
            )
        return None

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
    
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BOMBA

class Bomba(arcade.Sprite):
    FASE_ESPERANDO = "esperando"
    FASE_DETONANDO = "detonando"
    NUM_FRAMES    = 12
    FRAME_W       = 64
    FRAME_H       = 64
    DUR_EXPLOSION = 0.6

    def __init__(self, start_x, start_y, radio_danno=80, danno=80,
                 tiempo_mecha=1.5, escala=1.0):
        super().__init__(scale=escala)

        sheet = arcade.load_spritesheet(
            os.path.join('assets', 'graphics', 'Bomba.png')
        )
        self._frames = sheet.get_texture_grid(
            size=(self.FRAME_W, self.FRAME_H),
            columns=self.NUM_FRAMES,
            count=self.NUM_FRAMES
        )
        self.texture = self._frames[0]

        self.center_x     = start_x
        self.center_y     = start_y
        self.radio_danno  = radio_danno
        self.danno        = danno
        self.tiempo_mecha = tiempo_mecha
        self._timer          = 0.0
        self._fase           = self.FASE_ESPERANDO
        self._danno_aplicado = False

    def on_update(self, delta_time, enemy_list=None, lista_corazones=None):
        self._timer += delta_time

        if self._fase == self.FASE_ESPERANDO:
            self.texture = self._frames[int(self._timer / 0.3) % 2]
            if self._timer >= self.tiempo_mecha:
                self._fase  = self.FASE_DETONANDO
                self._timer = 0.0

        elif self._fase == self.FASE_DETONANDO:
            frames_explosion = self._frames[2:]
            progreso = self._timer / self.DUR_EXPLOSION
            idx = min(int(progreso * len(frames_explosion)), len(frames_explosion) - 1)
            self.texture = frames_explosion[idx]

            if not self._danno_aplicado and enemy_list is not None:
                for enemy in enemy_list:
                    dx = enemy.center_x - self.center_x
                    dy = enemy.center_y - self.center_y
                    dist = math.sqrt(dx**2 + dy**2) - (enemy.width / 2)
                    if dist <= self.radio_danno:
                        # Spawneamos corazón solo si va a morir
                        if lista_corazones is not None and enemy.health - self.danno <= 0:
                            from arma import CorazonVida
                            corazon = CorazonVida(enemy.center_x, enemy.center_y)
                            lista_corazones.append(corazon)
                        enemy.recibir_danno(self.danno)
                self._danno_aplicado = True  # ← solo se ejecuta UNA vez

            if self._timer >= self.DUR_EXPLOSION:
                self.kill()


class LanzaBombas(ArmaDistancia):
    def __init__(self):
        super().__init__(
            cooldown = 2.0,
            imagen   = os.path.join('assets', 'objects', 'lanza.png'),
            escala   = 0.4,
            nombre   = "Bomba"
        )
        sheet = arcade.load_spritesheet(
            os.path.join('assets', 'graphics', 'Bomba.png')
        )
        frames = sheet.get_texture_grid(
            size=(64, 64),
            columns=12,
            count=12
        )
        self.texture = frames[0]

    def disparar(self, player_sprite):
        return Bomba(
            start_x      = player_sprite.center_x,
            start_y      = player_sprite.center_y,
            radio_danno  = 40,
            danno        = 80,
            tiempo_mecha = 1.5,
            escala       = 2.0
        )


 # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BOOMERANG

class Boomerang(Proyectil):
    NUM_FRAMES = 2
    FRAME_W    = 16
    FRAME_H    = 16

    def __init__(self, start_x, start_y, direccion):
        super().__init__(
            velocidad = 7,
            rango     = 300,
            danno     = 35,
            imagen    = os.path.join('assets', 'graphics', 'Boomerang.png'),
            escala    = 3
        )
        self.center_x = start_x
        self.center_y = start_y
        self.direccion = direccion

        # Cargamos los frames de animación
        sheet = arcade.load_spritesheet(
            os.path.join('assets', 'graphics', 'Boomerang.png')
        )
        self._frames = sheet.get_texture_grid(
            size=(self.FRAME_W, self.FRAME_H),
            columns=self.NUM_FRAMES,
            count=self.NUM_FRAMES
        )
        self.texture = self._frames[0]
        self._anim_timer = 0.0

        # Dirección de movimiento
        if direccion == 0:
            self.change_x = self.velocidad
        elif direccion == 1:
            self.change_x = -self.velocidad
        elif direccion == 2:
            self.change_y = -self.velocidad
        elif direccion == 3:
            self.change_y = self.velocidad

    def update(self, delta_time):
        # Movimiento y comprobación de rango (heredado de Proyectil)
        super().update(delta_time)

        # Animación: alterna entre frame 0 y 1 cada 0.1s
        self._anim_timer += delta_time
        self.texture = self._frames[int(self._anim_timer / 0.1) % self.NUM_FRAMES]


class LanzaBoomerang(ArmaDistancia):
    def __init__(self):
        super().__init__(
            cooldown = 1,
            imagen   = os.path.join('assets', 'objects', 'lanza.png'),  # temporal
            escala   = 0.4,
            nombre   = "Boomerang"
        )
        sheet = arcade.load_spritesheet(
            os.path.join('assets', 'graphics', 'Boomerang.png')
        )
        frames = sheet.get_texture_grid(
            size=(16, 16),
            columns=2,
            count=2
        )
        self.texture = frames[0]

    def disparar(self, player_sprite):
        return Boomerang(
            start_x   = player_sprite.center_x,
            start_y   = player_sprite.center_y,
            direccion = player_sprite.facing_direction
        )

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CORAZÓN DE VIDA
class CorazonVida(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(scale=2.0)
        sheet = arcade.load_spritesheet(
            os.path.join('assets', 'graphics', 'Vida.png')
        )
        frames = sheet.get_texture_grid(
            size=(16, 16),
            columns=1,
            count=1
        )
        self.texture = frames[0]
        self.center_x = x
        self.center_y = y
        self.curacion = 10