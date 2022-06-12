from abc import abstractmethod

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

    def __init__(self, team):
        self.team = team
        self.power = 0
        self.position = None
        self.observations = None

    def get_team(self):
        return 'R' if self.team == self.RED else 'B'

    def get_id(self):
        return self.id
    
    def get_power(self):
        return self.power
    
    def get_position(self):
        return self.position

    def set_position(self, x, y):
        self.position = (x,y)
    
    def increase_power(self):
        self.power += 1
    
    def set_power(self, power):
        self.power = power

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
        