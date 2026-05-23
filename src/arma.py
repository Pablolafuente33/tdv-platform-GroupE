import arcade
import os




class ArmaCuerpoACuerpo(arcade.Sprite): #base para varias armas cuerpo a cuerpo 
    def __init__(self, danno , rango , cooldown, imagen, escala, nombre):        
        super().__init__(imagen, escala)
        self.danno = danno
        self.rango = rango
        self.cooldown_max = cooldown
        self.nombre = nombre
        self.cooldown = 0
        self.atacar = True

    def getDanno(self):
        return self.danno

    def on_update(self, delta_time):
        if self.cooldown > 0:
            self.cooldown -= delta_time
            self.atacar = False
        if self.cooldown <= 0:
            self.atacar = True


    def use(self, enemy_list, player_sprite):
        if self.atacar:
            self.center_x = player_sprite.center_x + (20 if player_sprite.change_x >= 0 else -20)
            self.center_y = player_sprite.center_y
            print("atacar")
            
            hit_list = arcade.check_for_collision_with_list(self, enemy_list)
            
            for enemy in hit_list:
                enemy.recibir_danno(self.danno)
                print(f"Enemigo dañado: {enemy.health} HP restantes")
            
            if hit_list:
                self.atacar = False 
                self.cooldown = self.cooldown_max

class Espada(ArmaCuerpoACuerpo):     
    def __init__(self):
        super().__init__(
            danno       = 30,
            rango       = 50,
            cooldown    = 4,
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
    
