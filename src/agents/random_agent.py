from agent import Agent
import random as rand

class RandomAgent(Agent):

    def __init__(self, team):
        super(RandomAgent, self).__init__(team)
    
    def action(self):
        return rand.randint(0, len(Agent.ACTIONS) - 1)
