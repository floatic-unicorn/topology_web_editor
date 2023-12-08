from model.topology import Topology, Vertex, Edge
from utils.geometry import euler_from_quaternion
import math

# Topology Constructor: Set origin data
def copy_map_data_from_yaml(map_data, topology: Topology):

    if 'resolution' in map_data:
        topology.resolution = map_data['resolution']
    else:
        raise ValueError('Map resolution not found in map data.')
    
    if 'origin' in map_data:
        topology.map_origin.append(map_data['origin'][0])
        topology.map_origin.append(map_data['origin'][1])
    else:
        raise ValueError('Map origin not found in map data.')

    if 'topology' in map_data:
        topology.topology_origin.append(map_data['topology']['origin']['position']['x'])
        topology.topology_origin.append(map_data['topology']['origin']['position']['y'])
        topology.topology_orient.append(map_data['topology']['origin']['orientation']['x'])
        topology.topology_orient.append(map_data['topology']['origin']['orientation']['y'])
        topology.topology_orient.append(map_data['topology']['origin']['orientation']['z'])
        topology.topology_orient.append(map_data['topology']['origin']['orientation']['w'])
    else:
        raise ValueError('Topology origin not found in map data.')

    return

# Topology Constructor: Set topology data
def copy_topology_data_from_yaml(src_topology, dst_topology: Topology):

    if 'Vertex' in src_topology:
        for idx in range(len(src_topology['Vertex'])):
            dst_topology.vertices[src_topology['Vertex'][idx]['id']] = Vertex( id = src_topology['Vertex'][idx]['id'],
                                                                               x = src_topology['Vertex'][idx]['x'],
                                                                               y = src_topology['Vertex'][idx]['y'])
            
    if 'Edge' in src_topology:
        for idx in range(len(src_topology['Edge'])):
            if src_topology['Edge'][idx]['src'] not in dst_topology.edges:
                dst_topology.edges[src_topology['Edge'][idx]['src']] = [Edge( src = src_topology['Edge'][idx]['src'],
                                                                              dst = src_topology['Edge'][idx]['dst'],
                                                                              cost = src_topology['Edge'][idx]['cost'],
                                                                              type = src_topology['Edge'][idx]['type'])]

            else:
                dst_topology.edges[src_topology['Edge'][idx]['src']].append( Edge( src = src_topology['Edge'][idx]['src'],
                                                                                   dst = src_topology['Edge'][idx]['dst'],
                                                                                   cost = src_topology['Edge'][idx]['cost'],
                                                                                   type = src_topology['Edge'][idx]['type']))
    return

def convert_topology_to_yaml(topology: Topology, topology_yml):

    vertex_list = [vertex for vertex in topology.vertices]
    edge_list = [edge for edge in topology.edges]

    for idx, id in enumerate(vertex_list):
        topology_yml['Vertex'][idx] = {}
        topology_yml['Vertex'][idx]['id'] = topology.vertices[id].id
        topology_yml['Vertex'][idx]['x'] = topology.vertices[id].x
        topology_yml['Vertex'][idx]['y'] = topology.vertices[id].y
        topology_yml['Vertex'][idx]['enabled'] = True
        topology_yml['Vertex'][idx]['frame_id'] = "map"
    
    count = 0
    for edge_src in edge_list:
        for edge in topology.edges[edge_src]:
            topology_yml['Edge'][count] = {}
            topology_yml['Edge'][count]['src'] = edge.src
            topology_yml['Edge'][count]['dst'] = edge.dst
            topology_yml['Edge'][count]['type'] = edge.type
            topology_yml['Edge'][count]['cost'] = edge.cost
            topology_yml['Edge'][count]['enabled'] = True
            count += 1

    return

# Return visualizable(map coordinate values) vertex & edge list
def get_raw_topology(topology: Topology):

    vertex_list = []
    edge_list = []

    for id in topology.vertices:
        x_val = (topology.vertices[id].x - topology.map_origin[0])/topology.resolution
        y_val = (topology.vertices[id].y - topology.map_origin[1])/topology.resolution

        _, _, yaw = euler_from_quaternion(topology.topology_orient[0],
                                          topology.topology_orient[1],
                                          topology.topology_orient[2],
                                          topology.topology_orient[3])

        x_val_ = (x_val - topology.topology_origin[0]) * math.cos(-yaw) - (y_val - topology.topology_origin[1]) * math.sin(-yaw)
        y_val_ = (x_val - topology.topology_origin[0]) * math.sin(-yaw) + (y_val - topology.topology_origin[1]) * math.cos(-yaw)

        vertex_list.append({'id': topology.vertices[id].id,
                            'x': x_val_,
                            'y': y_val_})
        
    for id in topology.vertices:

        if id not in topology.edges:
            continue

        edges = topology.edges[id]

        for edge in edges:
            edge_list.append({'src': edge.src,
                              "dst": edge.dst,
                              'cost': edge.cost})
            
    return vertex_list, edge_list