

import arcade
import os

class ArmaCuerpoACuerpo(arcade.Sprite): #base para varias armas cuerpo a cuerpo 
    def __init__(self, danno , rango , cooldown, imagen, escala, nombre):        
        super().__init__(imagen, escala)
        self.danno = danno
        self.rango = rango
        self.cooldown_max = cooldown
        self.nombre = nombre
        self.cooldown = 0 #Inicializamos el cooldown a 0 para que pueda usarse de primeras
        self.atacar = True

    def getDanno(self):
        return self.danno

    def on_update(self, delta_time):
        if self.cooldown > 0:
            self.cooldown -= delta_time
            self.atacar = False
        if self.cooldown <= 0:
            self.atacar = True
            self.cooldown = 0
        #arcade.check_for_collision_with_list(self.ArmaCuerpo_lista, self.enemigo_lista) #hay que implementar el enemigo

    def use(self):
        if self.atacar:
            self.atacar = False 
            self.cooldown = self.cooldown_max 

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Esto es lo que se va a ver que va a ir viajando por la pantalla

class Proyectil(arcade.Sprite): #base para proyectiles de armas a distancia
    def __init__(self, velocidad, rango, danno, imagen, escala):
        super().__init__(imagen, escala)
        self.danno = danno
        self.velocidad = velocidad
        self.rango = rango
    def on_update(self):
        self.rango -= 1
        if self.rango <= 0:
            self.kill()
    def getDanno(self):
        return self.danno

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Esto es lo que va a lanzar el proyectil
class ArmaDistancia(arcade.Sprite): #base para varias armas a distancia 

    def __init__(self, imagen, escala, cooldown):
        super().__init__(imagen, escala)
        self.cooldown = cooldown
        self.atacar = True
    
    def on_update(self, delta_time):
        if self.cooldown > 0:
            self.cooldown -= delta_time #Le restamos el tiempo real que ha pasado.
            self.atacar = False

        if self.cooldown <= 0:
            self.cooldown = 0
            self.atacar = True

    def getCooldown(self):
        return self.atacar
    

class Espada(ArmaCuerpoACuerpo):     
    def __init__(self):
        super().__init__(
            danno       = 30,
            rango       = 50,
            cooldown    = 0.8,
            imagen      = os.path.join('assets','espada.png'),
            escala      = 0.4,
            nombre      = "Espada",
        )
