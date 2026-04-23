

import arcade



class ArmaCuerpoACuerpo(arcade.Sprite): #base para varias armas cuerpo a cuerpo 
    def __init__(self, danno , rango , cooldown, imagen, escala):        
        super().__init__(imagen, escala)
        self.danno = danno
        self.rango = rango
        self.cooldown = cooldown
        self.atacar = True

    def getDanno(self):
        return self.danno

    def on_update(self, delta_time):
        if self.cooldown > 0:
            self.cooldown -= 1
            self.atacar = False
        if self.cooldown == 0:
            self.atacar = True
        #arcade.check_for_collision_with_list(self.ArmaCuerpo_lista, self.enemigo_lista) #hay que implementar el enemigo


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


class ArmaDistancia(arcade.Sprite): #base para varias armas a distancia 

    def __init__(self, imagen, escala, cooldown):
        super().__init__(imagen, escala)
        self.cooldown = cooldown
        self.atacar = True
    
    def on_update(self, delta_time):
        if self.cooldown > 0:
            self.cooldown -= 1
            self.atacar = False

        if self.cooldown == 0:
            self.atacar = True

    def getCooldown(self):
        return self.atacar
