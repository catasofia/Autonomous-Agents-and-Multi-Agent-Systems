import math
from agent import Agent
import random as rand
import numpy as np
from scipy.spatial.distance import cityblock

class GreedyAgent(Agent):

    def __init__(self, id, team, env, num_agents):
        super(GreedyAgent, self).__init__(id, team, env)
        self.num_agents = num_agents
    
    def action(self):
        pellets_positions = []
        enemys_positions = []
        for x in range(len(self.observations)):
            for y in range(len(self.observations[x])):
                if self.observations[x][y] == 2: 
                    pellets_positions.append((x,y))
                elif self.observations[x][y] >= 3  + (self.num_agents) and self.observations[x][y] <= 3 + self.num_agents * 2 - 1:
                    enemys_positions.append((x,y))
        closest_pellet, dist_pellet = self.closest_object(self.position, pellets_positions)
        closest_enemy, dist_enemy = self.closest_object(self.position, enemys_positions)
        if(closest_pellet is None or dist_enemy < dist_pellet):
            return self.direction_to_go(self.position, closest_enemy)
        elif(dist_pellet <= dist_enemy):
            return self.direction_to_go(self.position, closest_pellet)
        else:
            raise Exception("Impossible to move to closest object")

    ### Auxiliary Methods

    def direction_to_go(self, agent_position, object_position):
        distances = np.array(object_position) - np.array(agent_position)
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
            if distance < min:
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