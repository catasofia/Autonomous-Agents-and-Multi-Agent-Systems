import math
from re import A
from agent import Agent
from astar_algorithm import Astar
import random as rand
import numpy as np
import copy
from scipy.spatial.distance import cityblock

class GreedyAgent(Agent):

    def __init__(self,team):
        super(GreedyAgent, self).__init__(team)
    
    def action(self):
        pellets_positions = []
        enemys_positions = []
        for x in range(len(self.observations)):
            for y in range(len(self.observations[x])):
                if self.observations[x][y] == 2: 
                    pellets_positions.append((x,y))
                elif isinstance(self.observations[x][y], Agent):
                    if self.get_team() != self.observations[x][y].get_team():
                        enemys_positions.append((x,y))
        
        closest_pellet, dist_pellet = self.closest_object(self.position, pellets_positions)
        closest_enemy, dist_enemy = self.closest_object(self.position, enemys_positions)
        
        maze = copy.deepcopy(self.observations)
        for x in range(len(maze)):
            for y in range(len(maze[x])):
                if maze[x][y] == 1:
                    maze[x][y] = 1000
                elif maze[x][y] != 0:
                    maze[x][y] = 0
        astar = Astar(maze)
        if(closest_pellet is None and closest_enemy is not None or dist_enemy <= dist_pellet):
            result = astar.run(self.position, closest_enemy)
            return self.direction_to_go(result[0], result[1])
        elif(dist_pellet < dist_enemy and closest_pellet is not None):
            result = astar.run(self.position, closest_pellet)
            return self.direction_to_go(result[0], result[1])
        else:
            return rand.randint(0, len(Agent.ACTIONS) - 1)

    ### Auxiliary Methods

    def direction_to_go(self, agent_position, object_position):
        distances = np.array(object_position) - np.array(agent_position)
        #distances = [int(object_position[0]) - int(agent_position[0]), int(object_position[1]) - int(agent_position[1])]
        abs_distances = np.absolute(distances)
        if abs_distances[0] > abs_distances[1]:
            return self._close_horizontally(distances)
        elif abs_distances[0] < abs_distances[1]:
            return self._close_vertically(distances)
        else:
            roll = rand.uniform(0, 1)
            return self._close_horizontally(distances) if roll > 0.5 else self._close_vertically(distances)

    def closest_object(self, agent_position, object_positions):
        min = math.inf
        closest_object_position = None
        n_object = len(object_positions)
        for p in range(n_object):
            object_position = object_positions[p]
            distance = cityblock(agent_position, object_position)
            x, y = object_position
            if distance < min and isinstance(self.observations[x][y], Agent) and self.get_power() > self.observations[x][y].get_power():
                min = distance
                closest_object_position = object_position
            elif distance < min and not isinstance(self.observations[x][y], Agent):
                min = distance
                closest_object_position = object_position
        return closest_object_position, min

    def _close_horizontally(self, distances):
        if distances[0] > 0:
            return self.DOWN
        elif distances[0] < 0:
            return self.UP
        else:
            return self.NOOP

    def _close_vertically(self, distances):
        if distances[1] > 0:
            return self.RIGHT
        elif distances[1] < 0:
            return self.LEFT
        else:
            return self.NOOP