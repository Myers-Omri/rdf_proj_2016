from json import JSONEncoder

class GraphObjectEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
