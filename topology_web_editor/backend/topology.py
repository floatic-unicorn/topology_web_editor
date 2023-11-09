from pydantic import BaseModel

class Vertex(BaseModel):
    id: str
    x: float
    y: float

class Edge(BaseModel):
    src: str
    dst: str
    cost: float
    type: str

class Topology:
    def __init__(self):
        self.vertices = {}
        self.edges = {}
        self.origin = [-37.602316, -32.087689]
        self.resolution = 0.05