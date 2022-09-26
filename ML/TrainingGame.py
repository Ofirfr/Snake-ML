from inspect import trace
from snake.Body import Body
from snake.Fruits import Fruits
import pygame as pg


class TrainingGame:
    training_body = Body()
    training_fruit_system = Fruits()

    def __init__(self):
        self.training_body = Body()
        self.training_fruit_system = Fruits()

    def take_step(self, action):
        # action 0 = dont change, 1 = left, -1 = right
        if action == 1:
            self.training_body.go_left()
        if action == -1:
            self.training_body.go_right()
        # self.draw_game()
        self.training_body.update_body()
        self.training_fruit_system.submit_body(self.training_body)
        if (self.training_body.collisions_found()):
            return (self.get_state(), 0, True, "Game Over - Collision")
        reward = 0
        if (self.training_body.fruit_eaten == True):
            reward = 1
        return (self.get_state(), reward, False, "Game Continues")

    def get_state(self):
        return (self.training_body, self.training_fruit_system.current_fruit_location)

    def draw_game(self):
        from snake.Game import HEIGHT, WIDTH, BODY_PART_SIZE, BODY_COLOR, FRUIT_COLOR
        training_window = pg.display.set_mode((WIDTH, HEIGHT))
        pixels = pg.PixelArray(training_window)
        if (self.training_fruit_system.fruit_exists):
            for x in range(1, BODY_PART_SIZE-1):
                for y in range(1, BODY_PART_SIZE-1):
                    pixels[self.training_fruit_system.current_fruit_location[0]+x,
                           self.training_fruit_system.current_fruit_location[1]+y] = FRUIT_COLOR
        for body_part in self.training_body.body_parts:
            for x in range(1, BODY_PART_SIZE-1):
                for y in range(1, BODY_PART_SIZE-1):
                    pixels[body_part[0]+x, body_part[1]+y] = BODY_COLOR
        pixels.close()
        pg.display.update()
