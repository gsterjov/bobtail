from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Metadata
from rasa_nlu.model import Interpreter as RasaInterpreter


class Interpreter(object):
    def __init__(self, ctx, config_path, model_path):
        self.ctx = ctx
        self.config = RasaNLUConfig(config_path)
        self.metadata = Metadata.load(model_path)
        self.interpreter = RasaInterpreter.load(self.metadata, self.config)

    def process(self, data):
        result = self.interpreter.parse(data)
        return {
            "intent": result["intent"]["name"],
            "confidence": result["intent"]["confidence"]
        }
