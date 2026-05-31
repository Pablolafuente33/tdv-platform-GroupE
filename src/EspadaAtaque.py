import arcade
import os
from constantes import UP, DOWN, RIGHT, LEFT

class EspadaAtaque(arcade.TextureAnimationSprite):
    def __init__(self, x, y, direccion, enemy_list):
        super().__init__()
        self.scale = 3
        self.danno = 10
        self.enemy_list = enemy_list
        self.timer = 0.5
        self.danno_aplicado = False

        sheet = arcade.load_spritesheet(os.path.join('assets', 'graphics', 'Espada.png'))
        
        fila_map = {
            UP: 1,
            DOWN: 0,
            LEFT: 2,
            RIGHT: 3
        }

        fila = fila_map[direccion]
        todas = sheet.get_texture_grid(size=(64, 64), columns=9, count=9 * fila + 9)
        texture_list = todas[fila * 9: fila * 9 + 9]
        frames = [arcade.TextureKeyframe(tex, duration=50) for tex in texture_list]
        self.animation = arcade.TextureAnimation(frames)

        self.center_x = x
        self.center_y = y

    def update(self, delta_time):
        if not self.danno_aplicado:
            golpeados = arcade.check_for_collision_with_list(self, self.enemy_list)
            for enemigo in golpeados:
                enemigo.recibir_danno(self.danno)
                self.danno_aplicado = True

        self.timer -= delta_time
        self.update_animation(delta_time)

        if self.timer <= 0:
            self.remove_from_sprite_lists()