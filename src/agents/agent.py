from env import Environment
from abc import abstractmethod
import numpy as np

class Agent:
    # Agent actions
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    NOOP = 4
    ACTIONS = [UP, DOWN, LEFT, RIGHT, NOOP]

    # Teams
    RED = 'R'
    BLUE = 'B'

    def __init__(self, id, team, env):
        self.id = id
        self.team = team
        self.power = 0
        self.position = self.deploy_agent_on_env(env)
        self.observations = None
    
    def deploy_agent_on_env(self, env):
        free_cells = env.get_free_cells()

        if(self.team == self.RED):
            free_cells = list(filter(lambda x: (x[1] <= Environment.WIDTH // 2 - 1), free_cells))
        elif(self.team == self.BLUE):
            free_cells = list(filter(lambda x: (x[1] >= Environment.WIDTH // 2), free_cells))
        
        x, y = free_cells[np.random.choice(len(free_cells))]
        env.set_cell_as_agent(x, y, self.get_id(), self.get_power())
        return (x,y)

    def get_team(self):
        return self.team

    def get_id(self):
        return self.id
    
    def get_power(self):
        return self.power
    
    def get_position(self):
        return self.position

    def set_new_position(self, x, y):
        self.position = (x,y)
    
    def increase_power(self):
        self.power+=1

    @abstractmethod
    def action(self):
        raise NotImplementedError()

    def see(self, observations):
        self.observations = observations

    def move(self, action):
        self.position = self.get_desired_outcome(action)
    
    def get_desired_outcome(self, action):
        x, y = self.get_position()
        if action == self.UP:
            return (x-1, y)
        elif action == self.DOWN:
            return (x+1, y)
        elif action == self.LEFT:
            return (x, y-1)
        elif action == self.RIGHT:
            return (x, y+1)
        elif action == self.NOOP:
            return (x,y)
        
        raise Exception("Error establishing desired outcome!")