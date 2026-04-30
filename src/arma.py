

import arcade
import personajes
import enemigo

#placeholder data





class ArmaCuerpoACuerpo(arcade.Sprite): #base para varias armas cuerpo a cuerpo 
    def __init__(self, danno , rango , cooldown, imagen, escala):        
        super().__init__(imagen, escala)
        self.danno = danno
        self.rango = rango
        self.cooldown = cooldown
        self.atacar = True
        self.cooldown_original = cooldown

    def on_update(self, delta_time):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.cooldown == 0:
            self.atacar = True
        if arcade.check_for_collision_with_list(self.ArmaCuerpo_lista, self.enemigo_lista) #hay que implementar el enemigo
            enemigo.Enemigo.self.health -= self.danno


    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and self.atacar == True:

            #insertamos el sprite de ataque aquí
            #alculamos la hitbox del arma
            #volvemos a poner el sprite inicial
            self.cooldown = self.cooldown_original
            self.atacar = False


class ArmaDistancia(arcade.Sprite): #solo sirve para cambiar el sprite
    def __init__(self,direccion, imagen, escala):
        super().__init__(imagen, escala)
        self.direccion = direccion



class Proyectil(arcade.Sprite): #sirve para crear proyectiles


    def __init__(self, imagen, escala, cooldown, danno, rango, direccion, X, Y):
        super().__init__(imagen, escala)
        self.cooldown = cooldown
        self.atacar = True
        self.cooldown_original = cooldown
        self.danno = danno
        self.rango = rango
        self.direccion = personajes.Protagonista.facing_direction
        self.center_x = X   
        self.center_y = Y

    def on_update(self, delta_time):

        #cooldown
        if self.cooldown > 0:
            self.cooldown -= 1
            self.atacar = False

        if self.cooldown == 0:
            self.atacar = True

        #rango
        if self.atacar == True:
            self.rango -= 1

        if self.rango <= 0:
            self.kill()
        
        #movimiento
        if self.direccion == 0: #derecha
            self.center_x += 5
        elif self.direccion == 1: #izquierda
            self.center_x -= 5
        elif self.direccion == 2: #arriba
            self.center_y += 5
        elif self.direccion == 3: #abajo
            self.center_y -= 5


        #colision
        #arcade.check_for_collision_with_list(self.Proyectil_lista, self.enemigo_lista) #hay que implementar el enemigo
            #vida_enemigo -= self.danno #hay que implementar el enemigo
            #self.kill() 

        for proyectil in self.proyectiles_list:
            choque = arcade.check_for_collision_with_list(proyectil, self.wall_list)

        if len(choque) > 0:
            proyectil.kill()


    def on_key_press(self, key, modifiers):        #hacer que solo pueda atacar en la direccion en la que mira el personaje
        if key == arcade.key.SPACE and self.atacar == True:
            #insertamos el sprite de ataque aquí


            self.cooldown = self.cooldown_original
            self.atacar = False
            self.direccion = personajes.Protagonista.facing_direction
            self.center_x = personajes.Protagonista.center_x
            self.center_y = personajes.Protagonista.center_y
