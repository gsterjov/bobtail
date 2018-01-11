class Utterance(object):
    def __init__(self):
        self.text = None
        self.intents = {}
        self.entities = []

    def parse(self, results):
        self.text = results["text"]
        self.entities = results["entities"]
        for intent in results["intent_ranking"]:
            self.intents[intent["name"]] = intent["confidence"]

    def intents_with_confidence(self, minimum_confidence):
        intent_names = []

        for name, confidence in self.intents.items():
            if confidence > minimum_confidence:
                intent_names.append(name)

        return intent_names

