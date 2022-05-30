import agent as ag
import numpy as np
import pygame

class Environment:
    # Map square grid size
    WIDTH = 16
    HEIGHT = 16

    # Map items
    FREE_SPACE = 0
    BLOCK = 1
    PELLET = 2
    FIRST_AGENT_ID = 3

    # Map items image paths
    BLOCK_IMG = "../imgs/block.jpg"
    PELLET_IMG = "../imgs/pellet.jpg"
    RED_FISH_IMG = "../imgs/red_fish.png"
    BLUE_FISH_IMG = "../imgs/blue_fish.png"
    
    # Agent teams
    RED = 'R'
    BLUE = 'B'

    # Map settings
    MAP1 = "M1"
    MAP2 = "M2"
    MAP3 = "M3"
    MAP_SETTING = {
        MAP1:np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]),

        MAP2:np.array([[1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
                       [1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
                       [1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
                       [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
                       [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
                       [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
                       [1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
                       [1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1]]),

        MAP3:np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
                       [0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0],
                       [0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
                       [0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0],
                       [0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0],
                       [0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0],
                       [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0],
                       [0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0],
                       [0,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
                       [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
    }

    def __init__(self, num_agents, map=1):
        # Initialize map internal representation
        self.map = self.MAP_SETTING.get(self.MAP2)

        if num_agents % 2 == 0:
            self.num_agents = num_agents
        else:
            raise Exception("Total number of agents must be an even number. Try again.")

        self.scatter_pellets()
        self.agent_id_counter = self.FIRST_AGENT_ID
        self.agents = {}
        self.team_red, self.team_blue = self.initialize_teams(num_agents)

        # Initialize map GUI
        self.grid_display = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("AASMA FISH AND CHIPS")
        pygame.display.get_surface().fill((200, 200, 200))  # background
        self.block = pygame.image.load(self.BLOCK_IMG)
        self.pellet = pygame.image.load(self.PELLET_IMG)
        self.red_fish = pygame.image.load(self.RED_FISH_IMG)
        self.blue_fish = pygame.image.load(self.BLUE_FISH_IMG)

        self.block = pygame.transform.scale(self.block, (25,25))
        self.pellet = pygame.transform.scale(self.pellet, (25,25))
        self.red_fish = pygame.transform.scale(self.red_fish, (25,25))
        self.blue_fish = pygame.transform.scale(self.blue_fish, (25,25))
        # red_fish = pygame.transform.rotate(red_fish, 90) - rotate

        self.grid_node_width = 25
        self.grid_node_height = 25

    # Randomly deploys pellets in the map
    def scatter_pellets(self):
        free_cells = self.get_free_cells()
        num_pellets = len(free_cells) // 10

        for _ in range(num_pellets):
            x, y = free_cells[np.random.choice(len(free_cells))]
            self.map[x][y] = self.PELLET
            free_cells = self.get_free_cells()
    
    # Returns list of unoccupied cells (i.e., cells that have neither blocks, pellets, nor agents)
    def get_free_cells(self):
        unoccupied_cells = []

        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == self.FREE_SPACE: 
                    unoccupied_cells.append((x,y))

        return unoccupied_cells
    
    def initialize_teams(self, num_agents):
        num_agents_per_team = num_agents // 2
        team_red, team_blue = [], []
        
        for _ in range(num_agents_per_team):
            team_red.append(self.initialize_agent(self.RED))
            team_blue.append(self.initialize_agent(self.BLUE))

        return (team_red, team_blue)
    
    def initialize_agent(self, team):
        free_cells = self.get_free_cells()

        if(team == self.RED):
            free_cells = list(filter(lambda x: (x[1] <= self.WIDTH // 2 - 1), free_cells))
        elif(team == self.BLUE):
            free_cells = list(filter(lambda x: (x[1] >= self.WIDTH // 2), free_cells))
        
        x, y = free_cells[np.random.choice(len(free_cells))]
        agent = ag.Agent(team, (x,y), self.agent_id_counter)
        self.agents[agent.get_id()] = agent
        self.agent_id_counter += 1
        self.map[x][y] = agent.get_id()
        return agent

    def draw_map(self):
        self.update_map_gui()

        while self.team_blue and self.team_red:
            action = input("Enter an action:")
            if int(action) == 0:
                self.step(self.agents.get(3), 0)
            elif int(action) == 1:
                self.step(self.agents.get(3), 1)
            elif int(action) == 2:
                self.step(self.agents.get(3), 2)
            elif int(action) == 3:
                self.step(self.agents.get(3), 3)
            elif int(action) == 4:
                self.step(self.agents.get(3), 4)
            else:
                raise Exception("Trolaro abafa a palhinha")
            self.update_map_gui()

    def get_agent(self, agent_id):
        return self.agents.get(agent_id)

    def delete_agent_from_env(self, agent_id):
        agent = self.agents.get(agent_id)

        if (agent in self.team_blue):
            self.team_blue.remove(agent)
        elif (agent in self.team_red):
            self.team_red.remove(agent)
        else:
            raise Exception("Error removing agent from team")

        del self.agents[agent_id]

    def createSquare(self, x, y, color):
        pygame.draw.rect(self.grid_display, color, [x, y, self.grid_node_width, self.grid_node_height])

    def update_map_gui(self):

        y = 0  # we start at the top of the screen
        for row in self.map:
            x = 0 # for every row we start at the left of the screen again
            for item in row:
                if item == 0:
                    self.createSquare(x, y, (255, 255, 255))
                elif item == self.BLOCK:
                    self.grid_display.blit(self.block, (x,y))
                elif item == self.PELLET:
                    self.grid_display.blit(self.pellet, (x,y))
                elif item >= self.FIRST_AGENT_ID and item <= self.agent_id_counter:
                    if self.agents.get(item).get_team() == self.RED:
                        self.grid_display.blit(self.red_fish, (x,y))
                    else:
                        self.grid_display.blit(self.blue_fish, (x,y))
                else:
                    self.createSquare(x, y, (0, 0, 0))
                x += self.grid_node_width # for ever item/number in that row we move one "step" to the right
            y += self.grid_node_height   # for every new row we move one "step" downwards

        #for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        run = False

        pygame.display.update()

    def step(self, agent, action):
        prev_pos_x, prev_pos_y = agent.get_position()
        desired_pos_x, desired_pos_y = agent.get_desired_outcome(action)

        if (self.has_block(desired_pos_x, desired_pos_y)):
            return self.map, False
        elif (self.has_pellet(desired_pos_x, desired_pos_y)):
            self.update_map_eaten_pellet(prev_pos_x, prev_pos_y, desired_pos_x, desired_pos_y, agent)
            return self.map, True
        elif self.cell_has_agent(desired_pos_x, desired_pos_y):
            if self.is_enemy(desired_pos_x, desired_pos_y, agent.get_team()):
                enemy = self.get_agent(self.map[desired_pos_x][desired_pos_y])
                if enemy.get_power() > agent.get_power():
                    self.map[prev_pos_x][prev_pos_y] = 0
                    self.delete_agent_from_env(agent.get_id())
                    enemy.increase_power() # check this out in the future
                elif enemy.get_power() <= agent.get_power():    
                    self.map[prev_pos_x][prev_pos_y] = 0
                    self.map[desired_pos_x][desired_pos_y] = agent.get_id()
                    agent.set_new_position(desired_pos_x, desired_pos_y)
                    agent.increase_power() # check this out in the future
                    self.delete_agent_from_env(enemy.get_id())
                else:
                    raise Exception("Error updating map")
        else:
            self.map[prev_pos_x][prev_pos_y] = 0
            self.map[desired_pos_x][desired_pos_y] = agent.get_id()
            agent.set_new_position(desired_pos_x, desired_pos_y)
    
    def has_block(self, x, y):
        return self.map[x][y] == self.BLOCK

    def has_pellet(self, x, y):
        return self.map[x][y] == self.PELLET
    
    def update_map_eaten_pellet(self, prev_x, prev_y, next_x, next_y, agent):
        self.set_cell_as_free_space(prev_x, prev_y)
        agent.set_new_position(next_x, next_y)
        agent.increase_power()
        self.set_cell_as_agent(next_x, next_y, agent.get_id())

    def set_cell_as_free_space(self, x, y):
        self.map[x][y] = self.FREE_SPACE

    def set_cell_as_agent(self, x, y, agent_id):
        self.map[x][y] = agent_id

    def cell_has_agent(self, x, y):
        return self.map[x][y] >= self.FIRST_AGENT_ID and self.map[x][y] <= self.agent_id_counter

    def is_enemy(self, x, y, team):
        agent = self.agents.get(self.map[x][y])

        if (team == self.RED):
            return agent in self.team_blue
        elif (team == self.BLUE):
            return agent in self.team_red
        else:
            raise Exception("Error checking if agent is an enemy!")

map = Environment(4, 1)
map.draw_map()
