from agent import Agent
import random as rand

class RandomAgent(Agent):

    def __init__(self, id, team, env):
        super(RandomAgent, self).__init__(id, team, env)
    
    def action(self):
        return rand.randint(0, len(Agent.ACTIONS) - 1)
