class Action(object):
    def parse(ctx, definition):
        if type(definition) is dict:
            action_type = list(definition)[0]
            value = definition[action_type]

            if action_type == "message":
                return MessageAction(value)
            elif action_type == "react":
                return ReactAction(ctx, value)
            elif action_type == "ask":
                return AskAction(ctx, value)
            elif action_type == "quit":
                return QuitAction(ctx)

        return None


class MessageAction(Action):
    def __init__(self, message):
        self.message = message

    def execute(self):
        yield {"type": "message", "data": self.message}


class ReactAction(Action):
    def __init__(self, ctx, node):
        self.ctx = ctx
        self.node = node

    def execute(self):
        node = self.ctx.find_node(self.node)
        yield from node.process()


class AskAction(Action):
    def __init__(self, ctx, value):
        self.ctx = ctx
        config = {}

        if type(value) is dict:
            config.update(value)
        else:
            config["question"] = value

        self.question = config.get("question", None)
        self.responses = config.get("responses", {})

    def execute(self):
        self.response = yield {"type": "ask", "data": self.question}
        for resp, node_name in self.responses.items():
            if resp == self.response:
                node = self.ctx.find_node(node_name)
                for proc in node.process():
                    self.response = yield proc

    def response_is_affirmed(self):
        return self.response['intent'] == 'yes'


class QuitAction(Action):
    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self):
        yield {"type": "quit", "data": None}
