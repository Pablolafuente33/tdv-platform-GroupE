import math

from pathlib import Path

import arcade

# Constants used to track the direction a character is facing
RIGHT_FACING = 0
LEFT_FACING = 1

class Character(arcade.Sprite):
    def __init__(self, name_folder, name_file):
        super().__init__()

        self.facing_direction = RIGHT_FACING
        self.cur_texture = 0

        main_path = f":resources:images/animated_characters/{name_folder}/{name_file}"
        
        # Guardamos la textura de que está quieto
        idle_texture = arcade.load_texture(f"{main_path}_idle.png")
        
        # Make pairs with left and right facing textures
        self.idle_texture_pair = idle_texture, idle_texture.flip_left_right()
        
        # Load textures for walking with left and right facing textures
        self.walk_textures = []
        for i in range(8):
            texture = arcade.load_texture(f"{main_path}_walk{i}.png")
            self.walk_textures.append((texture, texture.flip_left_right()))

        self.climbing_textures = (
            arcade.load_texture(f"{main_path}_climb0.png"),
            arcade.load_texture(f"{main_path}_climb1.png")
        )

        # This variable will change dynamically and will represent the currently
        # active texture.
        self.texture = self.idle_texture_pair[0]


class Protagonista(Character):
    def __init__(self):
        super().__init__("female_adventurer", "femaleAdventurer")

        self.should_update_walk = 0

        # Nuevos atributos
        self.health = 100
        self.max_health = 100
        self.inventory = ["Pistola", "Escopeta", "Granada"] # Items de ejemplo
        self.equipped_index = 0

    def update_animation(self, delta_time):

        #Dirección según el movimiento horizontal
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        #Si no se mueve
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Si se mueve → animación de caminar
        self.should_update_walk += 1
        if self.should_update_walk >= 3:
            self.should_update_walk = 0
            self.cur_texture = (self.cur_texture + 1) % 8
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
    