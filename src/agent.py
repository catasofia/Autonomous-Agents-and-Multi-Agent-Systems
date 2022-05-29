from argparse import Action
from abc import ABC, abstractmethod

from numpy import power

class Agent:

    ACTIONS = {
        "UP":0,
        "DOWN":1,
        "LEFT":2,
        "RIGHT":3,
        "NOOP":4,
    }

    def __init__(self, team, position, id):
        self.team = team
        self.power = 0
        self.position = position
        self.id = id
    
    @abstractmethod
    def action(self) -> int:
        raise NotImplementedError()

    def move(self, action):
        x, y = self.position
        desired_outcome = self.get_desired_outcome(action)

        self.position = desired_outcome

    def get_team(self):
        return self.team

    def get_id(self):
        return self.id
    
    def get_power(self):
        return self.power
    
    def get_position(self):
        return self.position
    
    def increase_power(self, value):
        power += value

    def get_desired_outcome(self, action):
        x, y = self.position

        """ match self.ACTIONS.get(action):
            case 0:
                return (x, y+1)
            case 1:
                return (x, y-1)
            case 2:
                return (x-1, y)
            case 3:
                return (x+1, y)
            case 4:
                return self.position
            case _:
                raise Exception("Error establishing desired outcome") """