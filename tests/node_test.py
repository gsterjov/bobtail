from bobtail.node import Node
from bobtail.actions import Action
from bobtail.utterance import Utterance

def test_node_response():
    action = Action("i'm a response")
    node = Node(action)
    assert node.action.respond() == "i'm a response"


def test_node_evaluation():
    action1 = Action("number 1")
    action2 = Action("number 2")
    node1 = Node(action1, ["intent1"])
    node2 = Node(action2, ["intent2"])
    root = Node(None)

    root.add_child_node(node1)
    root.add_child_node(node2)

    utterance = Utterance()
    utterance.parse({
        "text": "i'm an utterance",
        "entities": [],
        "intent_ranking": [
            {"name": "intent1", "confidence": 0.1},
            {"name": "intent2", "confidence": 0.4},
        ]
    })

    assert root.satisfies(utterance) == True
    assert root.interpret(utterance) == "number 2"
