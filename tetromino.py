from typing import Any
from settings import *
import random

class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino
        self.pos = vec(pos) + INIT_POS_OFFSET
        self.next_pos = vec(pos) + NEXT_POS_OFFSET
        self.alive = True

        # Initializing sprite group
        super().__init__(tetromino.tetris.sprite_group)
        self.image = tetromino.image
        self.rect = self.image.get_rect()

        # Visual effects when scored
        self.sfx_image = self.image.copy()
        self.sfx_image.set_alpha(110)

        # Managing speed and cycle of visual effects (randomized)
        self.sfx_speed = random.uniform(0.3, 0.75)
        self.sfx_cycles = random.randrange(5, 7)

        self.cycle_counter = 0
        
    # Checks if visual effects has completed its cycles
    def sfx_end_time(self):
        if self.tetromino.tetris.app.animation_trigger:
            self.cycle_counter += 1
            if self.cycle_counter > self.sfx_cycles:
                self.cycle_counter = 0
                return True

    # Runs visual effects
    def sfx_run(self):
        self.image = self.sfx_image
        self.pos.y -= self.sfx_speed
        self.image = pg.transform.rotate(self.image, pg.time.get_ticks() * self.sfx_speed)

    # Checks if the block is alive (not cleared)
    def is_alive(self):
        if not self.alive: # If cleared, run the visual effects
            if not self.sfx_end_time():
                self.sfx_run()
            else:
                self.kill()

    # Rotates the block around a specified pivot point
    def rotate(self, pivot_pos):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos

    def set_rect_pos(self):
        pos = [self.next_pos, self.pos][self.tetromino.current]
        self.rect.topleft = pos * TILE_SIZE

    # Checks if block is alive and updates rectangle's position
    def update(self):
        self.is_alive()
        self.set_rect_pos()

    # Checks if blocks collide with game field, return True if there is
    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < FIELD_W and y < FIELD_H and (y < 0 or not self.tetromino.tetris.field_array[y][x]):
            return False
        return True

class Tetromino:
    # Initialization of class Tetromino, which takes tetris and current as parameters
    def __init__(self, tetris, current=True):
        self.tetris = tetris
        self.shape = random.choice(list(TETROMINOES.keys())) #Randomized tetromino shapes
        self.image = random.choice(tetris.app.images) #Randomized tetromino colors
        self.blocks = [Block(self, pos) for pos in TETROMINOES[self.shape]]
        self.landing = False
        self.current = current

    def rotate(self): # Rotates the tetrominoes
        pivot_pos = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

        # Checks for collision after rotation
        if not self.is_collide(new_block_positions):
            for i, block, in enumerate(self.blocks):
                block.pos = new_block_positions[i]

    # Checks if tetromino collides with game field
    def is_collide(self, block_positions): 
        return any(map(Block.is_collide, self.blocks, block_positions))

    # Moves the tetrominoes in a specified direction
    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_positions)

        if not is_collide:
            for block in self.blocks:
                block.pos += move_direction
        elif direction == 'down':
            self.landing = True

    # Updates the tetromino by moving it down
    def update(self):
        self.move(direction='down')
