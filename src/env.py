from turtle import width
import agent as ag
import numpy as np
import pygame

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
                free_cells = list(filter(lambda x: (x[1] <= (round(self.WIDTH / 2) - 1)), free_cells))
            case self.BLUE:
                free_cells = list(filter(lambda x: (x[1] >= round(self.WIDTH / 2)), free_cells))
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
    
    def has_agent_diff_team(self, x, y, team):
        agent_id = self.map[x][y]
        if (team == self.RED):
            return agent_id in self.team_blue
        elif (team == self.BLUE):
            return agent_id in self.team_red
        else:
            raise Exception("Team not valid")

    def draw_map(self):

        gridDisplay = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("AASMA FISH AND CHIPS")
        pygame.display.get_surface().fill((200, 200, 200))  # background
        block = pygame.image.load("../imgs/block.jpg")
        pellet = pygame.image.load("../imgs/pellet.jpg")
        red_fish = pygame.image.load("../imgs/red_fish.png")
        blue_fish = pygame.image.load("../imgs/blue_fish.png")

        block = pygame.transform.scale(block, (25,25))
        pellet = pygame.transform.scale(pellet, (25,25))
        red_fish = pygame.transform.scale(red_fish, (25,25))
        blue_fish = pygame.transform.scale(blue_fish, (25,25))
        # red_fish = pygame.transform.rotate(red_fish, 90) - rotate

        grid_node_width = 25
        grid_node_height = 25

        def createSquare(x, y, color):
            pygame.draw.rect(gridDisplay, color, [x, y, grid_node_width, grid_node_height ])

        y = 0  # we start at the top of the screen
        for row in self.map:
            x = 0 # for every row we start at the left of the screen again
            for item in row:
                if item == 0:
                    createSquare(x, y, (255, 255, 255))
                elif item == self.BLOCK:
                    gridDisplay.blit(block, (x,y))
                elif item == self.PELLET:
                    gridDisplay.blit(pellet, (x,y))
                elif item >= self.FIRST_AGENT_ID and item < self.agent_counter + self.FIRST_AGENT_ID:
                    if self.agents.get(item).get_team() == self.RED:
                        gridDisplay.blit(red_fish, (x,y))
                    else:
                        gridDisplay.blit(blue_fish, (x,y))
                else:
                    createSquare(x, y, (0, 0, 0))
                x += grid_node_width # for ever item/number in that row we move one "step" to the right
            y += grid_node_height   # for every new row we move one "step" downwards
        pygame.display.update()

        while True:
            pass

        """ for x in range(16):
            for y in range(16):
                if self.map[x][y] == 0:
                    print(" ", end=" ")
                elif self.map[x][y] == self.BLOCK:
                    print('H', end=" ")
                    screen.blit(block, x, y)
                elif self.map[x][y] == self.PELLET:
                    print('P', end=" ")
                elif self.map[x][y] >= self.FIRST_AGENT_ID and self.map[x][y] < self.agent_counter + self.FIRST_AGENT_ID:
                    if self.agents.get(self.map[x][y]).get_team() == self.RED:
                        print('R', end=" ")
                    else:
                        print('B', end=" ")
                else:
                    pygame.draw.rect(screen, (255, 0, 0), x, y, self.WIDTH)
                    raise Exception("Deu merda!")
            print("") """

    def get_free_cells(self):
        unoccupied_cells = []
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 0: unoccupied_cells.append((x,y))
        return unoccupied_cells

    def step(self, agent, action):
        # ver posicao atual do agente
        # ver se futura posicao está livre
            #se pellet, move e mais forte
            #se agente mais fraco, move e come o outro
            #se agente mais forte, morre
            #se free, move
            #else, não move
        (x,y) = agent.get_position()
        if action ==  0:
            (nx,ny) = (x, y+1)
        elif action ==  1:
            (nx,ny) = (x, y-1)
        elif action ==  2:
            (nx,ny) = (x-1, y)
        elif action == 3:
            (nx,ny) = (x+1, y)
        elif action == 4:
            (nx,ny) = (x,y)
        else:
            raise Exception("Error establishing desired outcome")
        
        if (self.has_block(nx, ny)):
            return self.map, False  
        
        elif (self.has_pellet(nx, ny)):
            agent.increase_power(5)
            self.map[nx][ny] = agent.get_id()
            self.map[x][y] = 0
            return self.map, True
        
        elif (self.map[nx][ny] > self.FIRST_AGENT_ID and self.map[x][y] < self.agent_counter + self.FIRST_AGENT_ID):
            self.has_agent_diff_team(nx, ny, agent.get_team())
        
        


map = Environment(4, 1)
map.draw_map()
