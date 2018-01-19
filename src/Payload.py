# Creates an easily accessible payload object from a dictionary
class Payload(object):
    def __init__(self, j):
        self.__dict__ = j


