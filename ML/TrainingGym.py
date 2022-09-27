from random import random
from ML.TrainingEnv import TrainingEnv
from keras.models import Sequential
from keras.layers import Flatten, Dense
from keras.optimizers import Adam
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
import numpy as np
import math

from snake.Game import BODY_PART_SIZE, WIDTH
EPISODES = 5
NUM_OF_STEPS = 10000
FILE_NAME = 'saved_agent.h5f'
# State is (fruit_location),(tail),....,(head)
NUM_OF_STATES = int(math.pow(WIDTH/BODY_PART_SIZE, 2))+1
ACTIONS = [-1, 0, 1]  # -1 = left, 0 = straight, 1 = right


class TrainingGym:

    def __init__(self):
        self.env = TrainingEnv()
        model = self.build_model(NUM_OF_STATES, len(ACTIONS))
        # model.summary()
        dqn = self.build_agent(model, len(ACTIONS))
        dqn.compile(Adam(learning_rate=1e-3), metrics=['mae'])
        dqn.load_weights(FILE_NAME)
        dqn.fit(self.env, nb_steps=NUM_OF_STEPS, visualize=False, verbose=1)

        scores = dqn.test(self.env, nb_episodes=EPISODES, visualize=False)
        print(np.mean(scores.history['episode_reward']))

        self.save_agent(dqn)

    def build_model(self, states, actions):
        model = Sequential()
        model.add(Flatten(name="InputLayer", input_shape=[1, states, 2, ]))
        model.add(Dense(32, name="FirstInternal", activation='relu'))
        model.add(Dense(32, name="SecondInternal", activation='relu'))
        model.add(Dense(actions, name="Prediction", activation='linear'))
        return model

    def build_agent(self, model, actions):
        policy = BoltzmannQPolicy()
        memory = SequentialMemory(limit=100000, window_length=1)
        dqn = DQNAgent(model=model,
                       memory=memory,
                       policy=policy,
                       nb_actions=actions,
                       nb_steps_warmup=100,
                       target_model_update=1e-3)
        return dqn

    def save_agent(self, dqn):
        dqn.save_weights(FILE_NAME, overwrite=True)
