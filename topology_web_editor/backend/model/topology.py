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
        self.map_origin = []
        self.topology_origin = []
        self.topology_orient = []
        self.resolution = 0.0

    def get_yaw(self):
        
        from utils.geometry import euler_from_quaternion
        _, _, yaw = euler_from_quaternion(self.topology_orient[0],
                                          self.topology_orient[1],
                                          self.topology_orient[2],
                                          self.topology_orient[3])
        
        return yaw