import arcade

# --- Constantes ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sandbox de Armas - Testing Hitboxes"

class Enemigo(arcade.Sprite):
    def __init__(self):
        super().__init__()
        # Textura roja para el enemigo
        self.texture = arcade.make_soft_circle_texture(40, arcade.color.RED_DEVIL)
        self.vida = 100
        self.center_x = 600
        self.center_y = 300

class Jugador(arcade.Sprite):
    def __init__(self, rapidez):
        super().__init__()
        # Textura azul para el jugador
        self.texture = arcade.make_soft_circle_texture(30, arcade.color.AZURE)
        self.rapidez = rapidez
        self.center_x = 200
        self.center_y = 300

    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y

class MiJuego(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)
        
        # Listas de sprites
        self.lista_jugador = arcade.SpriteList()
        self.lista_enemigos = arcade.SpriteList()
        
        self.jugador = None
        self.enemigo = None

    def setup(self):
        # Configurar Jugador
        self.jugador = Jugador(rapidez=5)
        self.lista_jugador.append(self.jugador)
        
        # Configurar Enemigo de prueba
        self.enemigo = Enemigo()
        self.lista_enemigos.append(self.enemigo)

    def on_draw(self):
        self.clear()
        
        # 1. Dibujar Sprites
        self.lista_jugador.draw()
        self.lista_enemigos.draw()
        
        # 2. DIBUJAR HITBOXES (Para debug)
        # Esto te permite ver el área real de colisión
        self.jugador.draw_hit_box(arcade.color.WHITE, line_thickness=2)
        if self.enemigo:
            self.enemigo.draw_hit_box(arcade.color.YELLOW, line_thickness=2)

        # 3. Info en pantalla
        arcade.draw_text(f"Enemigo Vida: {self.enemigo.vida}", 10, 570, arcade.color.WHITE, 12)
        arcade.draw_text("TECLA 'ESPACIO' PARA TESTEAR ATAQUE", 10, 20, arcade.color.WHITE, 10)

    def on_update(self, delta_time):
        self.lista_jugador.update()
        
    def on_key_press(self, key, modifiers):
        # MOVIMIENTO BÁSICO
        if key == arcade.key.UP: self.jugador.change_y = self.jugador.rapidez
        elif key == arcade.key.DOWN: self.jugador.change_y = -self.jugador.rapidez
        elif key == arcade.key.LEFT: self.jugador.change_x = -self.jugador.rapidez
        elif key == arcade.key.RIGHT: self.jugador.change_x = self.jugador.rapidez
        
        # ESPACIO PARA PROBAR TUS ARMAS
        elif key == arcade.key.SPACE:
            self.testear_arma()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.DOWN): self.jugador.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT): self.jugador.change_x = 0

    def testear_arma(self):
        """
        Aquí es donde TÚ programarás tus armas.
        Ejemplo de detección de colisión simple:
        """
        if arcade.check_for_collision(self.jugador, self.enemigo):
            print("¡Impacto detectado!")
            self.enemigo.vida -= 10
            if self.enemigo.vida <= 0:
                self.enemigo.remove_from_sprite_lists()

def main():
    game = MiJuego()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()