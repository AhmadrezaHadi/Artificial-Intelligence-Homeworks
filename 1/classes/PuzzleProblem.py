import networkx as nx
from matplotlib import pyplot as plt
import queue

# from networkx.classes.function import neighbors
# from networkx.classes.graph import Graph


class PuzzleProblem():
    def __init__(self, size, agent_loc, target_loc, wall_loc) -> None:
        self.size = size
        self.agent_loc = agent_loc
        self.target_loc = target_loc
        self.wall_locations = wall_loc
        self.path = []
        self.dls_path = []

        self.search_G = nx.grid_2d_graph(self.size, self.size)
        self.search_pos = {(x,y):(y,-x) for x,y in self.search_G.nodes()}
        # self.search_color_map = ['lightgreen' for _ in range(self.size * self.size)]

        self.G = nx.grid_2d_graph(self.size, self.size)
        self.pos = {(x,y):(y,-x) for x,y in self.G.nodes()}
        self.color_map = ['lightgreen' for _ in range(self.size * self.size)]

        self.color_map[self.agent_loc[0]*8 + self.agent_loc[1]] = 'orange'
        self.color_map[self.target_loc[0]*8 + self.target_loc[1]] = 'lightblue'
        
        for wall in self.wall_locations:
            self.color_map[wall[0]*8+wall[1]] = 'red'

            self.search_G.remove_node(wall)
            del self.search_pos[wall]

        self.search_G.nodes()[self.agent_loc]["start"] = True
        self.search_G.nodes()[self.target_loc]["end"] = True
   
    def drawPuzzle(self):
        if not self.path and not self.dls_path:
            nx.draw(self.G, pos=self.pos, 
            node_color=self.color_map, 
            with_labels=True,
            node_size=600)
        else:
            if self.path:
                self.color_map_bfs = self.color_map.copy()
                for node in self.path:
                  self.color_map_bfs[node[0]*8 + node[1]] = 'black'
                nx.draw(self.G, pos=self.pos, 
                node_color=self.color_map_bfs, 
                with_labels=True,
                node_size=600)
            if self.dls_path:
                self.color_map_dls = self.color_map.copy()
                for node in self.dls_path[1:-1]:
                    self.color_map_dls[node[0]*8 + node[1]] = 'blue'
                nx.draw(self.G, pos=self.pos, 
                node_color=self.color_map_dls, 
                with_labels=True,
                node_size=600)


    def drawSearchPuzzle(self):
        nx.draw(self.search_G, 
        pos=self.search_pos, 
        with_labels=True,
        node_size=600)
    
    def __returnPath(self):
        path = []
        current = self.target_loc
        while current != self.agent_loc:
            father = self.search_G.nodes()[current]["from"]
            current = father
            path.append(current)
        self.path = [i for i in reversed(path)][1:]
        return self.path

    def bfs(self):
        self.dls_path = []
        current = self.agent_loc
        visited = []
        visited.append(current)
        q = queue.Queue()
        if current == self.target_loc:
            return 2
        while current != self.target_loc:
            neighbors = [e[1] for e in self.search_G.edges(current)]
            for n in neighbors:
                if n == self.target_loc:
                    self.search_G.nodes()[n]["from"] = current
                    return self.__returnPath()

                if n not in visited:
                    self.search_G.nodes()[n]["from"] = current
                    visited.append(n)
                    q.put(n)
            if q.empty():
                return 0
            current = q.get()

    
    def DLS(self, node, depth, visited: list):
        if node == self.target_loc:
            self.dls_path.append(node)
            return 1
        if depth == 0:
            return -1
        if node not in visited:
            visited.append(node)
            neighbors = [e[1] for e in self.search_G.edges(node)]
            for n in neighbors:
                if n not in visited:
                    if self.DLS(node=n, depth=depth-1, visited=visited.copy()) == 1:
                        self.dls_path.append(node)
                        return 1
        return 0

    def IDS(self):
        i = 0
        self.path = []
        while self.DLS(node=self.agent_loc, depth=i, visited=[]) != 1:
            i = i+1
        return [i for i in reversed(self.dls_path[1:-1])]
        