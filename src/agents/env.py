import numpy as np
import pygame
import copy

# TODO:
# Decide what to do when agents from the same team cross paths with one another
# Think about alternate ways for represeneting incremental value of agent's power (how to represent it visually?)
# Refactor init

class Environment:
    # Map square grid size (in cells)
    WIDTH = 16
    HEIGHT = 16

    # Map items
    FREE_SPACE = 0
    BLOCK = 1
    PELLET = 2
    FIRST_AGENT_ID = 3

    # Map items image paths
    PELLET_IMG = "../../imgs/pellet.jpg"
    RED_FISH_IMG = "../../imgs/red_fish.png"
    BLUE_FISH_IMG = "../../imgs/blue_fish.png"
    CHIPS_IMG = "../../imgs/chips.jpg"
    BLOCK_IMG = "../../imgs/block.jpg"
    
    # Agent teams
    RED = 'R'
    BLUE = 'B'

    team_red = {}
    team_blue = {}

    def __init__(self, num_agents, map=1):
        # Initialize map internal representation
        MAP1 = "M1"
        MAP2 = "M2"
        MAP3 = "M3"
        MAP_SETTING = {
            MAP1:[[1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
                  [1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
                  [1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
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
                  [1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
                  [1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
                  [1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1]],

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
        self.map = MAP_SETTING.get(MAP2)
        self.num_agents = num_agents
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
                raise Exception("Impossible action!")
            self.update_map_gui()

    def createSquare(self, x, y, color):
        pygame.draw.rect(self.grid_display, color, [x, y, self.grid_node_width, self.grid_node_height])

    def update_map_gui(self):
        y = 0  # we start at the top of the screen
        for row in self.map:
            x = 0 # for every row we start at the left of the screen again
            for item in row:
                if item == 0:
                    self.createSquare(x, y, (255, 255, 255))
                elif not isinstance(item, tuple) and item == self.BLOCK:
                    self.grid_display.blit(self.block, (x,y))
                elif not isinstance(item, tuple) and item == self.PELLET:
                    self.grid_display.blit(self.pellet, (x,y))
                elif isinstance(item, tuple) and item[0] >= self.FIRST_AGENT_ID and item[0] < self.FIRST_AGENT_ID + self.num_agents:
                    if item[0] in self.team_red:
                        self.grid_display.blit(self.red_fish, (x,y))
                    elif item[0] in self.team_blue:
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
                enemy_pos = self.map[desired_pos_x][desired_pos_y]
                enemy = self.get_agent(enemy_pos[0], agent.get_team())
                if enemy.get_power() > agent.get_power():
                    self.set_cell_as_free_space(prev_pos_x, prev_pos_y)
                    self.delete_agent_from_env(agent.get_id(), agent.get_team())
                    enemy.increase_power()
                    self.set_cell_as_agent(desired_pos_x, desired_pos_y, enemy.get_id(), enemy.get_power())
                    return self.get_map(), self.is_game_over(), agent
                
                elif enemy.get_power() <= agent.get_power():
                    self.set_cell_as_free_space(prev_pos_x, prev_pos_y)
                    agent.increase_power()
                    self.set_cell_as_agent(desired_pos_x, desired_pos_y, agent.get_id(), agent.get_power())
                    agent.set_new_position(desired_pos_x, desired_pos_y)
                    self.delete_agent_from_env(enemy.get_id(), enemy.get_team())
                    return self.get_map(), self.is_game_over(), enemy
                
                else:
                    raise Exception("Error updating map!")
            else:
                return self.get_map(), self.is_game_over(), False
        
        elif self.cell_is_free(desired_pos_x, desired_pos_y):
            self.set_cell_as_free_space(prev_pos_x, prev_pos_y)
            self.set_cell_as_agent(desired_pos_x, desired_pos_y, agent.get_id(), agent.get_power())
            agent.set_new_position(desired_pos_x, desired_pos_y)
            return self.get_map(), self.is_game_over(), False
        
        else:
            raise Exception("Error updating map!")
    
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
        agent.set_new_position(next_x, next_y)
        agent.increase_power()
        self.set_cell_as_agent(next_x, next_y, agent.get_id(), agent.get_power())

    def set_cell_as_free_space(self, x, y):
        self.map[x][y] = self.FREE_SPACE

    def set_cell_as_agent(self, x, y, agent_id, agent_power):
        self.map[x][y] = (agent_id, agent_power)

    def cell_has_agent(self, x, y):
        #return self.map[x][y][0] >= self.FIRST_AGENT_ID and self.map[x][y][0] <= self.FIRST_AGENT_ID + self.num_agents
        return isinstance(self.map[x][y], tuple)

    def is_enemy(self, x, y, team):
        agent = self.map[x][y]
        if (team == self.RED):
            return agent[0] >= self.FIRST_AGENT_ID  + (self.num_agents // 2) and agent[0] <= self.FIRST_AGENT_ID + self.num_agents - 1
        elif (team == self.BLUE):
            return agent[0] >= self.FIRST_AGENT_ID and agent[0] <= self.FIRST_AGENT_ID + (self.num_agents // 2) - 1
        raise Exception("Error checking if agent is an enemy!")

    def get_agent(self, agent_id, team):
        if (team == self.RED):
            return self.team_blue.get(agent_id)
        elif (team == self.BLUE):
            return self.team_red.get(agent_id)  
        raise Exception("Error getting agent!")

    def delete_agent_from_env(self, agent_id, agent_team):
        if (agent_team == self.RED):
            del self.team_red[agent_id]
        elif (agent_team == self.BLUE):
            del self.team_blue[agent_id]
        else:
            raise Exception("Error deleting agent from environment!")

    def is_game_over(self):
        return len(self.team_red) == 0 or len(self.team_blue) == 0

    def cell_is_free(self, x, y):
        return self.map[x][y] == self.FREE_SPACE

    def get_map(self):
        return self.map
    
    def close(self):
        pygame.quit()
        #exit()

#map = Environment(4, 1)
#map.draw_map()
