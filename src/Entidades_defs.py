"""
Este archivo es más una base de datos de todas los sprites necesarios 
"""
import main
import arcade
from constantes import VELOCIDAD_CAMINAR_JUGADOR

ENTIDADES_DEFS = {
    'player' : {
        'velovidad_caminar' :VELOCIDAD_CAMINAR_JUGADOR,
        'animaciones' : {
            # walk  (Lua base 1 → Python base 0, restamos 1)
            'walk-down':  {'frames': [31, 32, 33, 34, 35, 36, 37, 38],   'interval': 0.15,  'texture': 'character-walk'},
            'walk-right': {'frames': [21, 22, 23, 24, 25, 26, 27, 28],   'interval': 0.15,  'texture': 'character-walk'},
            'walk-up':    {'frames': [11, 12, 13, 14, 15, 16, 17, 18],  'interval': 0.15,  'texture': 'character-walk'},
            'walk-left':  {'frames': [41, 42, 43, 44, 45, 46, 47, 48],      'interval': 0.155, 'texture': 'character-walk'},
            # idle
            'idle-down':  {'frames': [0],  'texture': 'character-walk'},
            'idle-right': {'frames': [4],  'texture': 'character-walk'},
            'idle-up':    {'frames': [8],  'texture': 'character-walk'},
            'idle-left':  {'frames': [12], 'texture': 'character-walk'},
            # sword
            
            #'sword-down':  {'frames': [0, 1, 2, 3],   'interval': 0.05, 'looping': False, 'texture': 'character-swing-sword'},
            #'sword-up':    {'frames': [4, 5, 6, 7],   'interval': 0.05, 'looping': False, 'texture': 'character-swing-sword'},
            #'sword-right': {'frames': [8, 9, 10, 11],  'interval': 0.05, 'looping': False, 'texture': 'character-swing-sword'},
            #'sword-left':  {'frames': [12, 13, 14, 15],'interval': 0.05, 'looping': False, 'texture': 'character-swing-sword'},
            
        }
    }
}