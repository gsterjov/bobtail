from bobtail.actions import Action


class Requirement(object):
    def parse(ctx, definition):
        required_node = definition["node"]
        unsatisfied_actions = []

        if "unsatisfied" in definition:
            for action_def in definition.get("unsatisfied", []):
                action = Action.parse(ctx, action_def)
                if action is not None:
                    unsatisfied_actions.append(action)

        return NodeRequirement(ctx, required_node, unsatisfied_actions)


class NodeRequirement(object):
    def __init__(self, ctx, required_node, unsatisfied_actions):
        self.ctx = ctx
        self.required_node = required_node
        self.unsatisfied = unsatisfied_actions
        self.fulfilled = False

    def process(self):
        node = self.ctx.find_node(self.required_node)
        yield from node.process()
        self.fulfilled = node.fulfilled()
