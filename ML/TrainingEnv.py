import re
from snake.Body import Body
from snake.Fruits import FRUIT_COLOR, NO_FRUIT_LOCATION, REWARD_PER_FRUIT, Fruits
import gym
from gym.spaces import Box
import numpy as np
import pygame as pg
import time
from snake.Game import BACKGROUND_COLOR, BODY_COLOR, BODY_PART_SIZE, HEAD_COLOR, WIN

BODY_INDICATOR = 1
FRUIT_INDICATOR = 2
HEAD_INDICATOR = 3



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
        # print(action)
        if action == 2:
            self.training_body.go_left()
        if action == 0:
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
        from snake.Game import WIDTH
        state = np.zeros((int(WIDTH/BODY_PART_SIZE+1),
                         int(WIDTH/BODY_PART_SIZE+1)))
        for body_part in self.training_body.body_parts:
            state[int(body_part[0]/BODY_PART_SIZE),
                  int(body_part[1]/BODY_PART_SIZE)] = BODY_INDICATOR
        head = self.training_body.body_parts[-1]
        state[int(head[0]/BODY_PART_SIZE),
                int(head[1]/BODY_PART_SIZE)] = HEAD_INDICATOR
        if (self.training_fruit_system.current_fruit_location != NO_FRUIT_LOCATION):
            state[int(self.training_fruit_system.current_fruit_location[0]/BODY_PART_SIZE),
                  int(self.training_fruit_system.current_fruit_location[1]/BODY_PART_SIZE)] = FRUIT_INDICATOR
        return state

    def reset(self):
        self.training_body = Body()
        self.training_fruit_system = Fruits()

        return self.get_state()

    def render(self, mode):
        time.sleep(0.05)
        if self.training_body.calc_reward() < 0:
            return
        WIN.fill(BACKGROUND_COLOR)
        pixels = pg.PixelArray(WIN)
        if (self.training_fruit_system.fruit_exists):
            for x in range(1, BODY_PART_SIZE-1):
                for y in range(1, BODY_PART_SIZE-1):
                    pixels[self.training_fruit_system.current_fruit_location[0]+x,
                           self.training_fruit_system.current_fruit_location[1]+y] = FRUIT_COLOR
        for body_part in self.training_body.body_parts:
            for x in range(1, BODY_PART_SIZE-1):
                for y in range(1, BODY_PART_SIZE-1):
                    pixels[body_part[0]+x, body_part[1]+y] = BODY_COLOR
        head = self.training_body.body_parts[-1]
        for x in range(1, BODY_PART_SIZE-1):
                for y in range(1, BODY_PART_SIZE-1):
                    pixels[head[0]+x, head[1]+y] = HEAD_COLOR
        pixels.close()
        pg.display.update()


    def close(self):
        pg.quit()
