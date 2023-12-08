from model.topology import Topology, Vertex, Edge
from utils.geometry import get_distance
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

        yaw =topology.get_yaw()

        x_val_ = (x_val - topology.topology_origin[0]) * math.cos(-yaw) - (y_val - topology.topology_origin[1]) * math.sin(-yaw)
        y_val_ = (x_val - topology.topology_origin[0]) * math.sin(-yaw) + (y_val - topology.topology_origin[1]) * math.cos(-yaw)

        vertex_list.append({'id': topology.vertices[id].id,
                            'x': x_val_,
                            'y': y_val_})
        
    for id in topology.vertices:
        if id not in topology.edges:
            continue

        for edge in topology.edges[id]:
            edge_list.append({'src': edge.src,
                              "dst": edge.dst,
                              'cost': edge.cost})
            
    return vertex_list, edge_list

def update_vertex(topology: Topology, id, dx, dy):

    yaw = topology.get_yaw()

    dx_ = dx * math.cos(yaw) - dy * math.sin(yaw)
    dy_ = dx * math.sin(yaw) + dy * math.cos(yaw)

    print("Update vertex {}".format(id))
    topology.vertices[id] = topology.vertices[id].update(dx_, dy_)

    return

def add_vertex(topology: Topology, x, y):

    ids = [int(id.split('_')[1]) for id in topology.vertices]
    if not ids:
        new_id = 'T_0'
    else:
        new_id = 'T_' + str(max(ids)+1)

    x = x * topology.resolution
    y = y * topology.resolution

    yaw = topology.get_yaw()

    x = x - topology.topology_origin[0]
    y = y - topology.topology_origin[1]

    x_ = x * math.cos(yaw) - y * math.sin(yaw)
    y_ = x * math.sin(yaw) + y * math.cos(yaw)


    x_ = x_ + topology.map_origin[0]
    y_ = y_ + topology.map_origin[1]

    print("Add new vertex {} at {},{}".format(new_id, x_, y_))
    topology.vertices[new_id] = Vertex(id = new_id, x = x_, y = y_)

    return new_id

def add_edge(topology: Topology, src, dst, cost, type):

    if src in topology.edges:
        topology.edges[src].append(Edge(src = src,
                                        dst = dst,
                                        cost = cost,
                                        type = type))
    else:
        topology.edges[src] = [Edge(src = src,
                                    dst = dst,
                                    cost = cost,
                                    type = type)]
                
    print("Add new edge from {} to {}".format(src, dst))
    return 

def connect_edges(topology: Topology, id_list, type):

    for i in range(len(id_list)-1):
        srcID = 'T_' + str(id_list[i])
        dstID = 'T_' + str(id_list[i+1])

        if srcID not in topology.vertices or dstID not in topology.vertices:
            continue

        cost = get_distance(topology.vertices[srcID],
                            topology.vertices[dstID])
        
        add_edge(topology, srcID, dstID, cost, type)
            
    return