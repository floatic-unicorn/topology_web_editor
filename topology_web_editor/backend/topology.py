from pydantic import BaseModel

class Vertex(BaseModel):
    id: str
    x: float
    y: float

    def update(self, x, y):
        self.x += x
        self.y += y
        return self

class Edge(BaseModel):
    src: str
    dst: str
    cost: float
    type: str

    def update_cost(self, cost):
        self.cost = cost

    def update_type(self, type):
        self.type = type

class Topology:
    def __init__(self):
        self.vertices = {}
        self.edges = {}
        self.origin = [-37.602316, -32.087689]
        self.resolution = 0.05