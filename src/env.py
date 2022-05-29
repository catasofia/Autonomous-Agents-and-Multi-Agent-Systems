import agent as ag
import numpy as np

class Environment:
    WIDTH = 16
    HEIGHT = 16

    BLOCK = 1
    PELLET = 2
    FIRST_AGENT_ID = 3

    RED = "RED"
    BLUE = "BLUE"

    def __init__(self, num_agents, map=1):
        block_disposition = {1: np.array([[1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],[1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],[1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],[0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],[0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],[1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],[1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],]), 2:"TODO", 3:"TODO"}
        self.map = block_disposition.get(map)
        self.num_agents = num_agents
        self.scatter_pellets()
        self.agent_counter = 0
        self.agents = {}
        self.team_red, self.team_blue = self.initialize_teams(num_agents)

    def scatter_pellets(self):
        free_cells = self.get_free_cells()
        num_pellets = round(len(free_cells) / 10)
        for _ in range(num_pellets):
            x, y = free_cells[np.random.choice(len(free_cells))]
            self.map[x][y] = 2
            free_cells = self.get_free_cells()

    def initialize_teams(self, total_num_agents):
        num_agents_per_team = round(total_num_agents / 2)
        team_red, team_blue = [], []
        
        for _ in range(num_agents_per_team):
            team_red.append(self.initialize_agent(self.RED))
            team_blue.append(self.initialize_agent(self.BLUE))

        return (team_red, team_blue)
    
    def initialize_agent(self, team):
        free_cells = self.get_free_cells()

        if(team == self.RED):
            free_cells = list(filter(lambda x: (x[1] <= (round(self.WIDTH / 2) - 1)), free_cells))
        elif(team == self.BLUE):
            free_cells = list(filter(lambda x: (x[1] >= round(self.WIDTH / 2)), free_cells))
        """ match team:
            case self.RED:
                free_cells = list(filter(lambda x: (x[0] <= (round(self.WIDTH / 2) - 1)), free_cells))
            case self.BLUE:
                free_cells = list(filter(lambda x: (x[0] >= round(self.WIDTH / 2)), free_cells))
            case _:
                raise Exception("Error initializing agent!") """
        
        x, y = free_cells[np.random.choice(len(free_cells))]
        agent = ag.Agent(team, (x,y), self.agent_counter + self.FIRST_AGENT_ID)
        self.agents[agent.get_id()] = agent
        self.agent_counter += 1
        self.map[x][y] = agent.get_id()
        return agent
        
    def has_block(self, x, y):
        return self.map[x][y] == 1

    def has_pellet(self, x, y):
        return self.map[x][y] == 2

    def draw_map(self):
        for x in range(16):
            for y in range(16):
                if self.map[x][y] == 0:
                    print(" ", end=" ")
                elif self.map[x][y] == self.BLOCK:
                    print('H', end=" ")
                elif self.map[x][y] == self.PELLET:
                    print('P', end=" ")
                elif self.map[x][y] >= self.FIRST_AGENT_ID and self.map[x][y] < self.agent_counter + self.FIRST_AGENT_ID:
                    if self.agents.get(self.map[x][y]).get_team() == self.RED:
                        print('R', end=" ")
                    else:
                        print('B', end=" ")
                else:
                    raise Exception("Deu merda!")
            print("")

    def get_free_cells(self):
        unoccupied_cells = []
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 0: unoccupied_cells.append((x,y))
        return unoccupied_cells

map = Environment(4, 1)
map.draw_map()