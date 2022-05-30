from abc import abstractmethod

class Agent:
    # Agent actions
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    NOOP = 4

    def __init__(self, team, position, id):
        self.team = team
        self.position = position
        self.id = id
        self.power = 0
    
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
    def action(self) -> int:
        raise NotImplementedError()

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
        else:
            raise Exception("Error establishing desired outcome!")