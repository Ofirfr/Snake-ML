from snake.Body import Body
from snake.Fruits import NO_FRUIT_LOCATION, Fruits
import gym
from gym.spaces import Box
import numpy as np

from snake.Game import BODY_PART_SIZE

REWARD_PER_FRUIT = 10
BODY_INDICATOR = 1
FRUIT_INDICATOR = 2


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
        if (self.training_fruit_system.current_fruit_location != NO_FRUIT_LOCATION):
            state[int(self.training_fruit_system.current_fruit_location[0]/BODY_PART_SIZE),
                  int(self.training_fruit_system.current_fruit_location[1]/BODY_PART_SIZE)] = FRUIT_INDICATOR
        return state

    def reset(self):
        self.training_body = Body()
        self.training_fruit_system = Fruits()

        return self.get_state()

    def render(self, mode):
        print("===============================================")
        print(self.get_state())
        print("===============================================")


    def close(self):
        return
