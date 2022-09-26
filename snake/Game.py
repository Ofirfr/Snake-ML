import pygame as pg
from snake.Body import Body

from snake.Fruits import FRUIT_COLOR, NO_FRUIT_LOCATION, Fruits
from snake.Direction import Direction
WIDTH, HEIGHT = 512, 512
WIN = pg.display.set_mode((WIDTH, HEIGHT))
BODY_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
BODY_PART_SIZE = 16
FPS = 10
pg.display.set_caption("Snake")


class Game:
    snake_body = Body()
    fruit_system = Fruits()

    def __init__(self):
        clock = pg.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        self.snake_body.go_left()
                    if event.key == pg.K_RIGHT:
                        self.snake_body.go_right()
            self.draw_game()
            self.snake_body.update_body()
            self.fruit_system.submit_body(self.snake_body)
            if (self.snake_body.collisions_found()):
                run = False
                print("Game Over - Collision found!")
        pg.quit()

    def draw_game(self):
        WIN.fill(BACKGROUND_COLOR)
        pixels = pg.PixelArray(WIN)
        if (self.fruit_system.fruit_exists):
            for x in range(1, BODY_PART_SIZE-1):
                for y in range(1, BODY_PART_SIZE-1):
                    pixels[self.fruit_system.current_fruit_location[0]+x,
                           self.fruit_system.current_fruit_location[1]+y] = FRUIT_COLOR
        for body_part in self.snake_body.body_parts:
            for x in range(1, BODY_PART_SIZE-1):
                for y in range(1, BODY_PART_SIZE-1):
                    pixels[body_part[0]+x, body_part[1]+y] = BODY_COLOR
        pixels.close()
        pg.display.update()
