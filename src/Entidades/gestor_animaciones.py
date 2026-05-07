import arcade

class Gestor_animaciones:
    def __init__(self, sprite, spritesheet_path, tamanno_sprite, rows, columns, count, duracion = 150) -> None:
        self.sprite = sprite
        sheet = arcade.load_spritesheet(spritesheet_path)

        self.animaciones = {
            "up": self.crear_anim(sheet, row=1, columns= columns, count= count, duracion= duracion, tamanno= tamanno_sprite),
            "right": self.crear_anim(sheet, row=2, columns= columns, count= count, duracion= duracion, tamanno= tamanno_sprite),
            "down": self.crear_anim(sheet, row=3, columns= columns, count= count, duracion= duracion, tamanno= tamanno_sprite),
            "left": self.crear_anim(sheet, row=4, columns= columns, count= count, duracion= duracion, tamanno= tamanno_sprite),
            "idle_down": self.crear_anim(sheet, row=0, columns= columns, count= count, duracion= duracion, tamanno= tamanno_sprite),
            "idle_left": self.crear_anim(sheet, row=4, columns= columns, count= count, duracion= duracion, tamanno= tamanno_sprite),
            "idle_right": self.crear_anim(sheet, row=4, columns= columns, count= count, duracion= duracion, tamanno= tamanno_sprite),
            "idle_up": self.crear_anim(sheet, row=4, columns= columns, count= count, duracion= duracion, tamanno= tamanno_sprite),

        }

        self.ultima_direccion = "down"
        self.sprite.animation = self.animaciones["idle_down"]

    def crear_anim(self, sheet, row, columns, count, duracion, tamanno):
        # Cargamos todos los frames de la sheet
        todas = sheet.get_texture_grid(size=tamanno, columns=columns, count=columns * row + count)
        # Cogemos solo los frames de la fila que nos interesa
        texture_list = todas[row * columns: row * columns + count]
        frames = [arcade.TextureKeyframe(tex, duration=duracion) for tex in texture_list]
        return arcade.TextureAnimation(frames)
    
    def update(self, change_x, change_y, delta_time):
        if change_x == 0 and change_y == 0:
            direccion = "idle_" + self.ultima_direccion
        elif abs(change_x) >= abs(change_y):
            self.ultima_direccion = "right" if change_x > 0 else "left"
            direccion = self.ultima_direccion
        else:
            self.ultima_direccion = "up" if change_y > 0 else "down"
            direccion = self.ultima_direccion

        new_anim = self.animaciones[direccion]
        if self.sprite.animation is not new_anim:
            self.sprite.animation = new_anim
        if not direccion.startswith("idle"):
            self.sprite.update_animation(delta_time)

