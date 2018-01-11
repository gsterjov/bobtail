from pyaml import yaml
from node import Node


class NodeTree(object):
    def __init__(self, introduction):
        self.introduction = introduction
        self.children = []
        self.definitions = None

    def load(self, definitions):
        with open(definitions, 'r') as f:
            self.definitions = yaml.load(f)

    def add_node(self, response, conditions=[]):
        node = Node(response)

        for condition in conditions:
            node.add_condition(condition)

        self.children.append(node)

        return node

    def print_tree(self):
        print(self.definitions)
        for node, defs in self.definitions["nodes"].items():
            print(node)
