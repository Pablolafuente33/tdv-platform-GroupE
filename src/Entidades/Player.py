'''
    Esta clase contiene todo lo relacionado al jugador:
    - Movimiento
    - De relación con objetos
    - etc.
'''
import arcade
import os
from pathlib import Path
from Entidades.gestor_animaciones import Gestor_animaciones
from constantes import PLAYER_SPEED
from arma import Espada
import math
# from constantes import PLAYER_SPEED

class Player(arcade.TextureAnimationSprite):
    def __init__(self):
        super().__init__()
        self.scale = 4.5

        #Se inicia gestor de animaciones, dando los valores generales del spritesheet para hacer las animaciones
        self.gestor_animaciones = Gestor_animaciones(
            sprite=self,
            spritesheet_path = os.path.join('assets','graphics','LinkSpriteSheet.png'),
            tamanno_sprite= (32, 32),
            columns= 9,
            duracion= 100
        )

        # Nuevos atributos
        self.health = 100
        self.max_health = 100
        self.inventario = [Espada()] + [None] * 4
        self.equipped_index = 0

    
    def objeto_siguiente(self):
        """Equipa el objeto posterior al que tenemos"""
        if self.inventario:
            self.equipped_index = (self.equipped_index + 1) % len(self.inventario)

    def objeto_anterior(self):
        """Equipa el objeto anterior al que tenemos"""
        if self.inventario:
            self.equipped_index = (self.equipped_index - 1) % len(self.inventario)

    def objeto_equipado(self):
        """ Nos da el objeto equipado"""
        if self.inventario:
            return self.inventario[self.equipped_index]
        return None
    
    def usar_objeto(self):
        """Usa el objeto equipado."""
        item = self.objeto_equipado()
        if item:
            item.use()

    def recoger_objeto(self, item):
        """
        Esto lo podemos implementar tanto para cuando nos encontremos encima de dicho objeto o 
        apretando un botón. Creo que al apretar un botón será mas complejo
        """
        for i in self.inventario:
            if i == None:
                i = item
    """
    ======================================================================================================
    ================================ ACTUALIZACIONES =====================================================
    ======================================================================================================
    """
    
    #Esto simplemente actualiza la animación que se este ejecutando
    def update_animation_state(self, delta_time):
        self.gestor_animaciones.update(self.change_x, self.change_y, delta_time)

    def actualizar_movimiento(self, up, down, left, right):
        #Determinamos la dirección del jugador.
        dir_x = 0
        dir_y = 0

        if up:
            dir_y +=1
        if down:
            dir_y -=1
        if left:
            dir_x -=1
        if right:
            dir_x += 1

        if dir_x !=0 and dir_y !=0:
            tam = math.sqrt(dir_x**2 + dir_y ** 2)

            self.change_x = (dir_x / tam) * PLAYER_SPEED
            self.change_y = (dir_y / tam) * PLAYER_SPEED
        else:
            self.change_x = dir_x * PLAYER_SPEED
            self.change_y = dir_y * PLAYER_SPEED

