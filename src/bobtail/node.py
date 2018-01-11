from requirement import Requirement
from actions import Action


class Node(object):
    def parse(ctx, definition):
        intents = set(definition.get("intents", []))
        requirements = []
        actions = []

        for req_def in definition.get("requirements", []):
            requirement = Requirement.parse(ctx, req_def)
            requirements.append(requirement)

        for action_def in definition.get("actions", []):
            action = Action.parse(ctx, action_def)
            if action is not None:
                actions.append(action)

        return DialogueNode(ctx, intents, requirements, actions)


class DialogueNode(object):
    def __init__(self, ctx, intents=[], requirements=[], actions=[]):
        self.ctx = ctx
        self.intents = intents
        self.requirements = requirements
        self.actions = actions

    def satisfies_intents(self, intents):
        if len(self.intents) > 0:
            return (set(intents) & self.intents) == self.intents
        return False

    def process(self):
        for requirement in self.requirements:
            yield from requirement.process()
            if not requirement.fulfilled:
                for action in requirement.unsatisfied:
                    yield from action.execute()

        for action in self.actions:
            yield from action.execute()

    def fulfilled(self):
        for requirement in self.requirements:
            if not requirement.fulfilled:
                return False

        for action in self.actions:
            if not action.response_is_affirmed():
                return False

        return True
