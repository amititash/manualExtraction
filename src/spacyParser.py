import spacy

class spacyParser(object):
    class __spacyParser:
        def __init__(self):
            self.val = None
    instance = None
    spacy_parser = None
    def __new__(cls): # __new__ always a classmethod
        if not spacyParser.instance:
            spacyParser.instance = spacyParser.__spacyParser()
            spacyParser.instance.spacy_parser = spacy.load("en")
        return spacyParser.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)