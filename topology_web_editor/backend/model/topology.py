from pydantic import BaseModel
import threading

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
        self.lock = threading.Lock()

    def get_yaw(self):
        
        from utils.geometry import euler_from_quaternion
        _, _, yaw = euler_from_quaternion(self.topology_orient[0],
                                          self.topology_orient[1],
                                          self.topology_orient[2],
                                          self.topology_orient[3])
        
        return yaw
    
    def get_new_id(self):
        ids = [int(id.split('_')[1]) for id in self.vertices]

        if not ids:
            new_id = 'T_0'
        else:
            new_id = 'T_' + str(max(ids)+1)

        return new_id
    
    def clear_map_data(self):
        self.map_origin = []
        self.topology_origin = []
        self.topology_orient = []
        self.resolution = 0.0

    def clear_topology_data(self):
        self.vertices = {}
        self.edges = {}

    def add_vertex(self, x_, y_):
        with self.lock:
            new_id = self.get_new_id()
            self.vertices[new_id] = Vertex(id = new_id,
                                            x = x_,
                                            y = y_)
        return new_id
            
    def remove_vertex(self, id):
        with self.lock:
            if id in self.vertices:
                del self.vertices[id]

            if id in self.edges:
                del self.edges[id]

            for edge_src in self.edges:
                for edge in self.edges[edge_src]:
                    if edge.dst == id:
                        del edge
        return

