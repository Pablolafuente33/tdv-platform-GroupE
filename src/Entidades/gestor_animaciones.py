'''
    Esta clase se encarga de generar las animaciones que utiliza de forma general toda entidad:
    - Idles.
    - Movimiento EN CUATRO DIRECCIONES.
'''

import arcade

class Gestor_animaciones:
    #Para usar la clase se deben dar los valores del sprite a usar (self), el path al archivo, el tamaño de los frames, la cantidad de
    #   columnas de frames componen la spritesheet, y finalmente la duración de la animación (cuanto menor, más rápido)
    def __init__(self, sprite, spritesheet_idle_path, tamanno_sprite, count, columns, duracion,
             spritesheet_atk_path=None, columns_atk=None, count_atk=None, duracion_atk=None, tamano_sprite_atk=None):
        self.sprite = sprite
        sheet = arcade.load_spritesheet(spritesheet_idle_path)

        self.animaciones = {
            "up": self.crear_anim(sheet, row=4, columns=columns, count=count, duracion=duracion, tamanno=tamanno_sprite),
            "right": self.crear_anim(sheet, row=5, columns=columns, count=count, duracion=duracion, tamanno=tamanno_sprite),
            "down": self.crear_anim(sheet, row=6, columns=columns, count=count, duracion=duracion, tamanno=tamanno_sprite),
            "left": self.crear_anim(sheet, row=7, columns=columns, count=count, duracion=duracion, tamanno=tamanno_sprite),
            "idle_down": self.crear_anim(sheet, row=3, columns=columns, count=1, duracion=duracion, tamanno=tamanno_sprite),
            "idle_left": self.crear_anim(sheet, row=2, columns=columns, count=1, duracion=duracion, tamanno=tamanno_sprite),
            "idle_right": self.crear_anim(sheet, row=1, columns=columns, count=1, duracion=duracion, tamanno=tamanno_sprite),
            "idle_up": self.crear_anim(sheet, row=0, columns=columns, count=1, duracion=duracion, tamanno=tamanno_sprite),
        }

        # Solo si se pasa spritesheet de ataque
        if spritesheet_atk_path is not None:
            sheet_atk = arcade.load_spritesheet(spritesheet_atk_path)
            self.animaciones.update({
                "attack_up":    self.crear_anim_ataque(sheet_atk, row=1, columns=columns_atk, count=count_atk, duracion=duracion_atk, tamano=tamano_sprite_atk),
                "attack_down":  self.crear_anim_ataque(sheet_atk, row=0, columns=columns_atk, count=count_atk, duracion=duracion_atk, tamano=tamano_sprite_atk),
                "attack_left":  self.crear_anim_ataque(sheet_atk, row=2, columns=columns_atk, count=count_atk, duracion=duracion_atk, tamano=tamano_sprite_atk),
                "attack_right": self.crear_anim_ataque(sheet_atk, row=3, columns=columns_atk, count=count_atk, duracion=duracion_atk, tamano=tamano_sprite_atk),
            })

        self.ultima_direccion = "down"
        self.sprite.animation = self.animaciones["idle_down"]

    #Esta es la funciñon que crea las animaciones dados los datos de la tabla
    def crear_anim(self, sheet, row, columns, count, duracion, tamanno):

        # Cargamos todos los frames de la sheet
        todas = sheet.get_texture_grid(size=tamanno, columns=columns, count=columns * row + count)
        
        # Cogemos solo los frames de la fila que nos interesa
        texture_list = todas[row * columns: row * columns + count]
        frames = [arcade.TextureKeyframe(tex, duration=duracion) for tex in texture_list]
        return arcade.TextureAnimation(frames)
    
    def crear_anim_ataque(self, sheet, row, columns, count, duracion, tamano):
        #Cargo los frames de la sheet,
        todas = sheet.get_texture_grid(size=tamano, columns=columns, count=columns * row + count)

        #Cojo los frames de la fila que interesa
        texture_list = todas[row * columns: row * columns + count]
        frames = [arcade.TextureKeyframe(tex, duration=duracion) for tex in texture_list]
        return arcade.TextureAnimation(frames)
    
    
    #Esta función se encarga de establecer las animaciones dependiendo de lo que haga el jugador. Es decir establece las animaciones
    # de cada tipo de movimiento.
    def update(self, change_x, change_y, delta_time):

        #Dependiendo de hacia que lado nos movamos la siguiente idle apuntará hacia el mismo lado
        if change_x == 0 and change_y == 0:
            direccion = "idle_" + self.ultima_direccion
        elif abs(change_x) >= abs(change_y):
            self.ultima_direccion = "right" if change_x > 0 else "left"
            direccion = self.ultima_direccion
        else:
            self.ultima_direccion = "up" if change_y > 0 else "down"
            direccion = self.ultima_direccion

        #Ahora comprobamos si es necesario cambiar la animación o si seguir con la actual
        new_anim = self.animaciones[direccion]
        if self.sprite.animation is not new_anim:
            self.sprite.animation = new_anim
        if not direccion.startswith("idle"):
            self.sprite.update_animation(delta_time)

    def update_ataque(self, delta_time):
        direccion_ataque = "attack_" + self.ultima_direccion
        new_anim = self.animaciones[direccion_ataque]
        if self.sprite.animation is not new_anim:
            self.sprite.animation = new_anim
        self.sprite.update_animation(delta_time)