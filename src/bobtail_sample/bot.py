import sys
sys.path.append('../')
sys.path.append('../bobtail')

from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer

from bobtail.node import Node
from bobtail.node_soup import NodeSoup
from bobtail.interpreter import Interpreter


def train():
    training_data = load_data('data/training/yes_no_simple.json')
    trainer = Trainer(RasaNLUConfig("config_spacy.json"))
    trainer.train(training_data)
    model_directory = trainer.persist(
        './data/models/')  # Returns the directory the model is stored in


def listen():
    interpreter = Interpreter(None, "config_spacy.json",
                              "./data/models/default/model_20180111-221428")
    soup = create_node_soup()

    nodes = soup.find_nodes("request_sleep")
    node = nodes[0]

    def do_interrupt(interrupt):
        if interrupt["type"] == "ask":
            answer = input("\U0001F419 {0} ".format(interrupt["data"]))
            interpreted_answer = interpreter.process(answer)
            return interpreted_answer
        elif interrupt["type"] == "message":
            print(interrupt["data"])
        elif interrupt["type"] == "quit":
            exit()

    gen = node.process()
    val = None
    try:
        while True:
            val = do_interrupt(gen.send(val))
    except StopIteration:
        pass


def create_node_soup():
    soup = NodeSoup("Hello")
    soup.load('./data/definitions.yml')
    return soup


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'train':
        train()
    else:
        listen()
