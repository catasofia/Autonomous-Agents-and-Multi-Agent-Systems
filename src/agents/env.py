import numpy as np
import pygame
from agent import Agent

# TODO:
# Decide what to do when agents from the same team cross paths with one another
# Refactor init

class Environment:
    # Map square grid size (in cells)
    WIDTH = 16
    HEIGHT = 16

    # Map items
    FREE_SPACE = 0
    BLOCK = 1
    PELLET = 2

    # Map items image paths
    PELLET_IMG = "../../imgs/pellet.jpg"
    RED_FISH_IMG = "../../imgs/red_fish.png"
    BLUE_FISH_IMG = "../../imgs/blue_fish.png"
    CHIPS_IMG = "../../imgs/chips.jpg"
    BLOCK_IMG = "../../imgs/block.jpg"
    
    def __init__(self, num_agents, map=1):
        # Initialize map internal representation
        MAP1 = "M1"
        MAP2 = "M2"
        MAP3 = "M3"
        MAP_SETTING = {
            MAP1:[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
            MAP2:[[1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
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
                  [1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1]],
            MAP3:[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        }        
        self.map = MAP_SETTING.get(MAP1)
        self.num_agents = num_agents
        self.red_team = num_agents // 2
        self.blue_team = self.red_team
        self.scatter_pellets()

        # Initialize map GUI
        self.grid_display = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("AASMA FISH AND CHIPS")
        pygame.display.get_surface().fill((200, 200, 200))  # background
        self.block = pygame.image.load(self.BLOCK_IMG)
        self.pellet = pygame.image.load(self.CHIPS_IMG)
        self.red_fish = pygame.image.load(self.RED_FISH_IMG)
        self.blue_fish = pygame.image.load(self.BLUE_FISH_IMG)

        self.block = pygame.transform.scale(self.block, (25,25))
        self.pellet = pygame.transform.scale(self.pellet, (25,25))
        self.red_fish = pygame.transform.scale(self.red_fish, (25,25))
        self.blue_fish = pygame.transform.scale(self.blue_fish, (25,25))
        self.blue_fish = pygame.transform.flip(self.blue_fish, True, False)

        self.grid_node_width = 25
        self.grid_node_height = 25

    # Randomly deploys pellets in the map
    def scatter_pellets(self):
        free_cells = self.get_free_cells()
        num_pellets = len(free_cells) // 10

        for _ in range(num_pellets):
            x, y = free_cells[np.random.choice(len(free_cells))]
            self.set_cell_as_pellet(x, y)
            free_cells = self.get_free_cells()
    
    # Returns list of unoccupied cells (i.e., cells that have neither blocks, pellets, nor agents)
    def get_free_cells(self):
        unoccupied_cells = []

        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == self.FREE_SPACE: 
                    unoccupied_cells.append((x,y))

        return unoccupied_cells

    def set_cell_as_pellet(self, x, y):
        self.map[x][y] = self.PELLET

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
                elif isinstance(item, Agent):
                    if item.get_team() == Agent.RED:
                        self.grid_display.blit(self.red_fish, (x,y))
                    elif item.get_team() == Agent.BLUE:
                        self.grid_display.blit(self.blue_fish, (x,y))
                else:
                    self.createSquare(x, y, (0, 0, 0))
                x += self.grid_node_width # for ever item/number in that row we move one "step" to the right
            y += self.grid_node_height   # for every new row we move one "step" downwards

        #for event in pygame.event.get():g
        #    if event.type == pygame.QUIT:
        #        run = False

        pygame.display.update()

    def step(self, agent, action):
        prev_pos_x, prev_pos_y = agent.get_position()
        desired_pos_x, desired_pos_y = agent.get_desired_outcome(action)
        
        if self.cell_is_out_of_map_bounds(desired_pos_x, desired_pos_y) or self.has_block(desired_pos_x, desired_pos_y):
            return self.get_map(), self.is_game_over(), False
        
        elif self.has_pellet(desired_pos_x, desired_pos_y):
            self.update_map_eaten_pellet(prev_pos_x, prev_pos_y, desired_pos_x, desired_pos_y, agent)
            return self.get_map(), self.is_game_over(), False
        
        elif self.cell_has_agent(desired_pos_x, desired_pos_y):

            if self.is_enemy(desired_pos_x, desired_pos_y, agent.get_team()):
                enemy = self.map[desired_pos_x][desired_pos_y]

                if enemy.get_power() > agent.get_power():
                    self.set_cell_as_free_space(prev_pos_x, prev_pos_y)
                    self.delete_agent_from_env(agent)
                    enemies = self.get_agents_from_team(enemy.get_team())
                    self.increase_team_power(enemies)
                    return self.get_map(), self.is_game_over(), agent
                
                elif enemy.get_power() <= agent.get_power():
                    self.set_cell_as_free_space(prev_pos_x, prev_pos_y)
                    self.set_cell_as_agent(desired_pos_x, desired_pos_y, agent)
                    agent.set_position(desired_pos_x, desired_pos_y)
                    agents = self.get_agents_from_team(agent.get_team())
                    self.increase_team_power(agents)
                    self.delete_agent_from_env(enemy)
                    return self.get_map(), self.is_game_over(), enemy
                
                else:
                    raise Exception("Error updating map!")

            else:
                return self.get_map(), self.is_game_over(), False
        
        elif self.cell_is_free(desired_pos_x, desired_pos_y):
            self.set_cell_as_free_space(prev_pos_x, prev_pos_y)
            self.set_cell_as_agent(desired_pos_x, desired_pos_y, agent)
            agent.set_position(desired_pos_x, desired_pos_y)
            return self.get_map(), self.is_game_over(), False
        
        else:
            raise Exception("Error updating map!")
    
    def get_agents_from_team(self, team):
        agents = []
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if isinstance(self.map[x][y], Agent):
                    agent = self.map[x][y]
                    if(agent.get_team() == team):
                        agents.append(agent)
        return agents

    def increase_team_power(self, agents):
        for agent in agents:
            agent.increase_power()

    def cell_is_out_of_map_bounds(self, x, y):
        is_x_out_of_map_bound = x > self.HEIGHT - 1 or x < 0 
        is_y_out_of_map_bound = y > self.WIDTH - 1 or y < 0
        return is_x_out_of_map_bound or is_y_out_of_map_bound

    def has_block(self, x, y):
        return self.map[x][y] == self.BLOCK

    def has_pellet(self, x, y):
        return self.map[x][y] == self.PELLET
    
    def update_map_eaten_pellet(self, prev_x, prev_y, next_x, next_y, agent):
        self.set_cell_as_free_space(prev_x, prev_y)
        agent.set_position(next_x, next_y)
        agents = self.get_agents_from_team(agent.get_team())
        self.increase_team_power(agents)
        self.set_cell_as_agent(next_x, next_y, agent)

    def set_cell_as_free_space(self, x, y):
        self.map[x][y] = self.FREE_SPACE

    def set_cell_as_agent(self, x, y, agent):
        self.map[x][y] = agent

    def cell_has_agent(self, x, y):
        return isinstance(self.map[x][y], Agent)

    def is_enemy(self, x, y, caller_team):
        agent = self.map[x][y]
        return caller_team != agent.get_team()

    def is_game_over(self):
        return self.red_team == 0 or self.blue_team == 0

    def cell_is_free(self, x, y):
        return self.map[x][y] == self.FREE_SPACE

    def get_map(self):
        return self.map
    
    def delete_agent_from_env(self, agent):
        if agent.get_team() == Agent.RED:
            self.red_team -= 1
        else:
            self.blue_team -= 1

    def close(self):
        pygame.quit()
        #exit()
