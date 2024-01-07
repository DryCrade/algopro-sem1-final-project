from settings import *
from tetris import Tetris, Text
import sys
import pathlib

# Music setup
pg.mixer.init()

pg.mixer.music.load('assets/music/tetris.ogg')
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(.35)

# Main Class Application
class App:
    
    # Initialization
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris')

        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.set_timer()
        self.images = self.load_images()
        
        self.tetris = Tetris(self)
        self.text = Text(self)

    # Loading the custom-made tetrominoes into the game
    def load_images(self):
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
        return images

    # Setting up timer for game events
    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1

        self.animation_trigger = False
        self.fast_animation_trigger = False

        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)

    # Updates the state of the game + Limiting FPS
    def update(self):
        self.tetris.update()
        self.clock.tick(FPS)
    
    # Drawing game elements
    def draw(self):
        self.screen.fill(color=BG_COLOR)
        self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))

        self.tetris.draw()
        self.text.draw()

        pg.display.flip()

    # Monitors Pygame events such as key presses, user events, and quit event
    def check_events(self):
        self.animation_trigger = False
        self.fast_animation_trigger = False

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.animation_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_animation_trigger = True
    
    # Main game loop (constantly checks for events, updates, and redraws)
    def run(self): 
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    app = App()
    app.run()