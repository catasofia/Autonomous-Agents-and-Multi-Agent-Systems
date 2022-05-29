from argparse import Action
from abc import ABC, abstractmethod

from numpy import power

class Agent:

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    NOOP = 4

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
    
    def increase_power(self):
        self.power+=1

    def get_desired_outcome(self, action):
        x, y = self.get_position()

        if action ==  self.UP:
            return (x-1, y)
        elif action ==  self.DOWN:
            return (x+1, y)
        elif action ==  self.LEFT:
            return (x, y-1)
        elif action ==  self.RIGHT:
            return (x, y+1)
        elif action ==  self.NOOP:
            return (x,y)
        else:
            raise Exception("Error establishing desired outcome")