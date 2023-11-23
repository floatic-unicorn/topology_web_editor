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
        self.map_origin = [-37.602316, -32.237689]
        self.topology_origin = [4.6374365045139419e-310, 
                                4.6374365045139419e-310]
        self.topology_orient = [4.6374365045139419e-310,
                                4.9406564584124654e-324,
                                4.9406564584124654e-324,
                                6.9531389063687279e-310]
        self.resolution = 0.05