from pyaml import yaml
from bobtail.node import Node


class NodeSoup(object):
    def __init__(self, introduction):
        self.introduction = introduction
        self.nodes = {}
        self.definitions = None

    def load(self, definitions):
        with open(definitions, 'r') as f:
            self.definitions = yaml.load(f)
            self.load_nodes()

    def load_nodes(self):
        for name, node_def in self.definitions["nodes"].items():
            self.nodes[name] = Node.parse(self, node_def)

    def find_nodes(self, intent):
        return [
            node for node in self.nodes.values()
            if node.satisfies_intents([intent])
        ]

    def find_node(self, name):
        return self.nodes[name]
