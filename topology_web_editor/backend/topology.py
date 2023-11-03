from pydantic import BaseModel

class Vertex(BaseModel):
    id: str
    x: float
    y: float
    enabled: bool

class Edge(BaseModel):
    src: str
    dst: str
    cost: float
    type: str

class Topology:
    def __init__(self):
        self.vertices = {}
        self.edges = {}
