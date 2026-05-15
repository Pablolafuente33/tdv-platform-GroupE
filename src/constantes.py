"""
    Aquí simplemente se establecen las constantes que más afectan al juego y se vayan a utilizar de forma seguida
"""
# constants.py

# Ventana
WINDOW_WIDTH  = 1280
WINDOW_HEIGHT = 704
WINDOW_TITLE  = "MEDIAVAL FIGTH"

# Tiles y habitación
TILE_SIZE    = 64
WALL_COLS    = WINDOW_WIDTH  // TILE_SIZE
WALL_ROWS    = WINDOW_HEIGHT // TILE_SIZE

ROOM_LEFT   = TILE_SIZE
ROOM_RIGHT  = WINDOW_WIDTH  - TILE_SIZE
ROOM_BOTTOM = TILE_SIZE
ROOM_TOP    = WINDOW_HEIGHT - TILE_SIZE
ROOM_W      = ROOM_RIGHT  - ROOM_LEFT
ROOM_H      = ROOM_TOP    - ROOM_BOTTOM

# Jugador
PLAYER_SPEED = 3
PLAYER_RADIUS         = 20
DOOR_TILES            = 3

# HUD
HUD_MARGIN    = (WINDOW_WIDTH // 2) - 161
HUD_BAR_W     = 260
HUD_BAR_H     = 20
HUD_SLOT_SIZE = 58
HUD_SLOT_GAP  = 8
HUD_SLOT_Y    = 16

# Colores
COLOR_WALL  = (60,  60,  60)
C_DARK      = (26,  18,   8)
C_GOLD      = (212, 160,  48)
C_GOLD_DIM  = (107,  74,  26)
C_HP_HIGH   = (200,  40,  40)
C_HP_MED    = (200, 120,   0)
C_HP_LOW    = (140,  16,  16)
C_SLOT_BG   = (30,  20,  10)
C_SLOT_EQ   = (42,  30,  12)
C_WHITE     = (255, 255, 255)
C_MUTED     = (160, 128,  64)