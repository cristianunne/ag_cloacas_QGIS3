import os

class PathClass():

    def __init__(self):
        self.path = None

    def getPath(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        return self.path