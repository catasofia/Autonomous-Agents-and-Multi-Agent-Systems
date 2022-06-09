import heapq

class Astar:

    class PriorityQueue:
        def __init__(self):
            self.elements = []

        def empty(self):
            return not self.elements

        def put(self, item, priority):
            heapq.heappush(self.elements, (priority, item))

        def get(self):
            return heapq.heappop(self.elements)[1]

    def __init__(self, map):
            self.map = self.convert_to_graph(map)

    def convert_to_graph(self, map):
        graph = {}
        for i in range(len(map)):
            for j in range(len(map[i])):
                if(map[i][j] != 1000):
                    current_node = (i,j)
                    graph[current_node] = self.create_neighbors(current_node, map)
        return graph

    def create_neighbors(self, node, map):
        x, y = node
        neighbors = []
        top = (x-1, y)
        bottom = (x+1, y)
        left = (x, y-1)
        right = (x, y+1)

        if not (x-1 < 0) and map[x-1][y] != 1000:
            neighbors.append(top)
        if not (x+1 >= len(map)) and map[x+1][y] != 1000:
            neighbors.append(bottom)
        if not (y-1 < 0) and map[x][y-1] != 1000:
            neighbors.append(left)
        if not (y+1 >= len(map[0])) and map[x][y+1] != 1000:
            neighbors.append(right)

        return neighbors

    def a_star_search(self, start, goal):
        frontier = self.PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break
            
            for next in self.get_neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(next, goal)
                    frontier.put(next, priority)
                    came_from[next] = current

        path = self.reconstruct_path(came_from, start, goal)
        return path

    def get_neighbors(self, current):
        return self.map[current]

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []

        while current != start:
            path.append(current)
            current = came_from[current]

        path.append(start)
        path.reverse()
        return path
        