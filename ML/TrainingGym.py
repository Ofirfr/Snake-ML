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
EPISODES = 100
NUM_OF_STEPS = 3000000
FILE_NAME = 'saved_agent.h5f'
# State is (fruit_location),(tail),....,(head)
NUM_OF_STATES = int(math.pow(WIDTH/BODY_PART_SIZE, 2))+1
ACTIONS = [0, 1, 2]  # 0 = left, 1 = straight, 2 = right


class TrainingGym:

    def __init__(self):
        self.env = TrainingEnv()
        model = self.build_model(NUM_OF_STATES, len(ACTIONS))
        # model.summary()
        dqn = self.build_agent(model, len(ACTIONS))
        dqn.compile(Adam(learning_rate=0.000146))
        dqn.load_weights(FILE_NAME)
        dqn.fit(self.env, nb_steps=NUM_OF_STEPS, visualize=False, verbose=1)

        scores = dqn.test(self.env, nb_episodes=EPISODES, visualize=False)
        print(np.mean(scores.history['episode_reward']))

        self.save_agent(dqn)

    def build_model(self, states, actions):
        model = Sequential()
        model.add(Flatten(name="InputLayer", input_shape=[
                  1, int(WIDTH/BODY_PART_SIZE+1), int(WIDTH/BODY_PART_SIZE+1), ]))
        model.add(Dense(16, name="FirstInternal", activation='relu'))
        model.add(Dense(16, name="SecondInternal", activation='relu'))
        model.add(Dense(actions, name="Prediction", activation='linear'))
        return model

    def build_agent(self, model, actions):
        policy = BoltzmannQPolicy()
        memory = SequentialMemory(limit=1000000000, window_length=1)
        dqn = DQNAgent(model=model,
                       memory=memory,
                       policy=policy,
                       nb_actions=actions
                       )
        return dqn

    def save_agent(self, dqn):
        dqn.save_weights(FILE_NAME, overwrite=True)
