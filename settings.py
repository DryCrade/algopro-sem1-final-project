import pygame as pg

vec = pg.math.Vector2

# Setting up global constants
FPS = 60
FIELD_COLOR = (59, 39, 32)
BG_COLOR = (51, 51, 51)

# Assets for custom-made tetrominoes and game font
SPRITE_DIR_PATH = 'assets/sprites'
FONT_PATH = 'assets/font/modern-tetris.ttf'

# Interval of falling blocks (normal + fast)
ANIM_TIME_INTERVAL = 450 #ms
FAST_ANIM_TIME_INTERVAL = 15 #ms

# Sizes of tile, field, and setting uup field resolution
TILE_SIZE = 50
FIELD_SIZE = FIELD_W, FIELD_H = 8, 16
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE

FIELD_SCALE_W, FIELD_SCALE_H = 1.7, 1.0
WIN_RES = WIN_W, WIN_H = FIELD_RES[0] * FIELD_SCALE_W, FIELD_RES[1] * FIELD_SCALE_H

# Setting up initial position offset and next position offset
INIT_POS_OFFSET = vec(FIELD_W // 2 - 1, 0)
NEXT_POS_OFFSET = vec(FIELD_W * 1.3, FIELD_H * 0.45)
MOVE_DIRECTIONS = {'left': vec(-1, 0), 'right': vec(1, 0), 'down': vec(0, 1)}

# Shape of tetrominoes
TETROMINOES = {
    '[': [(0, 0), (1, 0), (0, 1), (0, 2), (1, 2)],
    'P': [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2)],
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)],
}