import logging
from logging import Logger

class Nodes():
    def __init__(self):
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)

    def __iadd__(self, l):
        self.nodes += l
        return self    

    def get_nodes(self, num):
        if num < len(self.nodes):
            return None

        tmp = self.nodes
        selected_nodes = []
        for i in range(0, num):
            select = random.randint(0, len(tmp))
            selected_nodes.append(tmp[select])
            del tmp[select]
        return selected_nodes