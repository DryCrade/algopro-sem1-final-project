from settings import *
import math
from tetromino import Tetromino
import pygame.freetype as ft

class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH) # Custom font for the game

    # Text placements
    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.02),text='TETRIS', fgcolor='white', size=TILE_SIZE * 1.07, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.65, WIN_H * 0.22),text='next', fgcolor='orange', size=TILE_SIZE * 1.1, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.67),text='score', fgcolor='orange', size=TILE_SIZE * 1.1, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.8),text=f'{self.app.tetris.score}', fgcolor='white', size=TILE_SIZE * 1.35)
        
class Tetris:
    # Creates a sprite group, initializes the game field array, and sets up the initial tetromino and next tetromino
    def __init__(self,app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.speed_up = False

        # Initializing scores to zero
        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500} # Point system

        pg.init()
        pg.mixer.init()
        self.rotate_sound = pg.mixer.Sound('assets/music/rotate.ogg')

    # Incrementing system for the score
    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0

    # Checking for full lines and removing them if detected
    def check_full_lines(self):
        row = FIELD_H - 1
        for y in range(FIELD_H - 1, -1, -1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]

                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)

            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
            else:
                for x in range(FIELD_W):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0

                self.full_lines += 1

    # Adds current tetromino blocks in the array
    def put_tetrominoes_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    # Creates and returns an empty 2D array 
    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]
    
    # Checks if game is over
    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(300)
            return True
    
    #Checks if tetromino has landed
    def check_tetromino_landing(self):
        if self.tetromino.landing:
            if self.is_game_over():
                self.__init__(self.app)
            else:
                self.speed_up = False
                self.put_tetrominoes_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)
        
    # Controls for playing the game
    def control(self, pressed_key):
        key_actions = {
            pg.K_LEFT: lambda: self.tetromino.move(direction='left'),
            pg.K_a: lambda: self.tetromino.move(direction='left'),
            pg.K_RIGHT: lambda: self.tetromino.move(direction='right'),
            pg.K_d: lambda: self.tetromino.move(direction='right'),
            pg.K_UP: lambda: self.rotate_tetromino(),
            pg.K_w: lambda: self.rotate_tetromino(),
            pg.K_DOWN: lambda: setattr(self, 'speed_up', True),
            pg.K_s: lambda: setattr(self, 'speed_up', True),
        }

        action = key_actions.get(pressed_key)
        if action:
            action()

    def rotate_tetromino(self):
        self.tetromino.rotate()
        self.rotate_sound.play()


    # Drawing the grid using black squares
    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'black', 
                             (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def update(self):
        event_trigger = [self.app.animation_trigger, self.app.fast_animation_trigger][self.speed_up]
        
        if event_trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()

    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)