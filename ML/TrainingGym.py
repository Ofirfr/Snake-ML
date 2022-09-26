from random import random
from ML.TrainingGame import TrainingGame

import random
EPISODES = 10000
class TrainingGym:
    q_table = {}
    def __init__(self):
        for episode in range (1,EPISODES+1):
            env = TrainingGame()
            env.__init__()
            state = env.get_state()
            done = False
            score = 0

            while not done:
                action = random.choice([-1,0,1])
                new_state, reward, done, info = env.take_step(action)
                score += reward
            if(score > 0):
                print("Episode:{} Score:{}".format(episode,score))