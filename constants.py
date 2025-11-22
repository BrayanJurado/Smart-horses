"""
Constantes y configuraciones del juego Smart Horses
"""

# Ventana
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

# Tablero
BOARD_SIZE = 8
CELL_SIZE = 70
BOARD_OFFSET_X = 50
BOARD_OFFSET_Y = 50

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT_COLOR = (186, 202, 68, 150)
MOVE_HIGHLIGHT = (130, 151, 105, 180)
DESTROYED_COLOR = (100, 100, 100)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 210)
TEXT_COLOR = (50, 50, 50)
POSITIVE_POINTS = (34, 139, 34)
NEGATIVE_POINTS = (220, 20, 60)

# Configuración del juego
POINT_VALUES = [-10, -5, -4, -3, -1, 1, 3, 4, 5, 10]
PENALTY_POINTS = 4

# Niveles de dificultad
DIFFICULTY_DEPTH = {
    "principiante": 2,
    "amateur": 4,
    "experto": 6
}