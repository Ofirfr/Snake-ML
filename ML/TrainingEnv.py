import re
from snake.Body import Body
from snake.Fruits import NO_FRUIT_LOCATION, Fruits
import pygame as pg
import gym
from gym.spaces import Box
import numpy as np

REWARD_PER_FRUIT = 10


class TrainingEnv(gym.Env):

    def __init__(self):
        self.training_body = Body()
        self.training_fruit_system = Fruits()

        from ML.TrainingGym import ACTIONS, NUM_OF_STATES
        self.observation_space = Box(low=0, high=2, shape=(2,))
        self.action_space = Box(low=0, high=len(ACTIONS), shape=(1,))

        self.state = self.get_state()

    def step(self, action):
        # action 0 = dont change, 1 = left, -1 = right
        if action == 1:
            self.training_body.go_left()
        if action == -1:
            self.training_body.go_right()
        self.training_body.update_body()
        self.training_fruit_system.submit_body(self.training_body)

        reward = self.training_body.calc_reward()
        if (reward < 0):
            return (self.get_state(), reward, True, {})
        if (self.training_body.fruit_eaten == True):
            reward += REWARD_PER_FRUIT
        return (self.get_state(), reward, False, {})

    def get_state(self):
        state = []
        for body_part in self.training_body.body_parts:
            state.append(list(body_part))
        state.insert(
            0, list(self.training_fruit_system.current_fruit_location))
        from ML.TrainingGym import NUM_OF_STATES
        state = state + [NO_FRUIT_LOCATION] * (NUM_OF_STATES-len(state))
        state = np.asarray(state)
        return state

    def reset(self):
        self.training_body = Body()
        self.training_fruit_system = Fruits()

        return self.get_state()

    def render(self, mode):
        if self.training_body.calc_reward():
            return
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

    def close(self):
        pg.quit()
