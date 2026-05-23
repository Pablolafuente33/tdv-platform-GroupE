import arcade
import os

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
        self.dur_ataque = 0.15


    def pos_arma(self, player_sprite):
        distancia = 30 # Separación del arma respecto al centro del jugador

        if player_sprite.facing_direction == RIGHT:
            self.center_x = player_sprite.center_x + distancia
            self.center_y = player_sprite.center_y
            self.angle = -45 #La iniciamos hacia delante
        if player_sprite.facing_direction == LEFT:
            self.center_x = player_sprite.center_x - distancia
            self.center_y = player_sprite.center_y
            self.angle = 45 #La iniciamos hacia delante
        if player_sprite.facing_direction == UP:
            self.center_x = player_sprite.center_x 
            self.center_y = player_sprite.center_y + distancia
            self.angle = 45 #La iniciamos hacia delante
        if player_sprite.facing_direction == DOWN:
            self.center_x = player_sprite.center_x 
            self.center_y = player_sprite.center_y - distancia
            self.angle = 225 #La iniciamos hacia delante
        
        
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
            if player_sprite is not None:
                self.pos_arma(player_sprite)


    def use(self, enemy_list, player_sprite):
        if self.atacar:
            # Colocamos el arma y activamos su temporizador visual
            self.pos_arma(player_sprite)
            self.tiempo_visible = self.dur_ataque
            
            hit_list = arcade.check_for_collision_with_list(self, enemy_list)
            
            for enemy in hit_list:
                enemy.recibir_danno(self.danno)
            
            self.atacar = False 
            self.cooldown = self.cooldown_max

class Espada(ArmaCuerpoACuerpo):     
    def __init__(self):
        super().__init__(
            danno       = 30,
            rango       = 50,
            cooldown    = 3,
            imagen      = os.path.join('assets','espada.png'),
            escala      = 0.4,
            nombre      = "Espada",
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
            self.cooldown -= delta_time #Le restamos el tiempo real que ha pasado.
            self.atacar = False

        if self.cooldown <= 0:
            self.cooldown = 0
            self.atacar = True

    def getCooldown(self):
        return self.atacar
    
