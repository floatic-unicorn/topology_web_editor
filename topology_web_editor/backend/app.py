from flask import Flask, request, jsonify
from flask_cors import CORS
import yaml
from topology import Topology, Vertex, Edge
from utils import euler_from_quaternion, get_distance
import math

app = Flask(__name__)
CORS(app)

topology_ = Topology()


@app.route('/load_topology', methods=['POST'])
def load_from_file():

    data = request.get_json()

    if 'filePath' not in data:
        return jsonify(success=False, error='No filepath provided')

    filename = data['filePath']

    with open(filename, 'r') as file:
        topology = yaml.safe_load(file)
        if topology is None:
            pass

    if 'Vertex' in topology:
        for idx in range(len(topology['Vertex'])):
            topology_.vertices[topology['Vertex'][idx]['id']] = \
                Vertex(id=topology['Vertex'][idx]['id'],
                x=topology['Vertex'][idx]['x'],
                y=topology['Vertex'][idx]['y'])
            
    if 'Edge' in topology:
        for idx in range(len(topology['Edge'])):
            if topology['Edge'][idx]['src'] not in topology_.edges:
                topology_.edges[topology['Edge'][idx]['src']] = \
                    [Edge(src=topology['Edge'][idx]['src'],
                        dst=topology['Edge'][idx]['dst'],
                        cost=topology['Edge'][idx]['cost'],
                        type=topology['Edge'][idx]['type'])]

            else:
                topology_.edges[topology['Edge'][idx]['src']].append( \
                    Edge(src=topology['Edge'][idx]['src'],
                        dst=topology['Edge'][idx]['dst'],
                        cost=topology['Edge'][idx]['cost'],
                        type=topology['Edge'][idx]['type']))

    return jsonify(success=True)

@app.route('/load_map_data', methods=['POST'])
def load_data_from_file():

    data = request.get_json()

    if 'filePath' not in data:
        return jsonify(success=False, error='No filepath provided')

    filename = data['filePath']

    with open(filename, 'r') as file:
        map_data = yaml.safe_load(file)
        if map_data is None:
            pass

    if 'resolution' in map_data:
        topology_.resolution = map_data['resolution']
    
    if 'origin' in map_data:
        topology_.map_origin.append(map_data['origin'][0])
        topology_.map_origin.append(map_data['origin'][1])

    if 'topology' in map_data:
        topology_.topology_origin.append(map_data['topology']['origin']['position']['x'])
        topology_.topology_origin.append(map_data['topology']['origin']['position']['y'])
        topology_.topology_orient.append(map_data['topology']['origin']['orientation']['x'])
        topology_.topology_orient.append(map_data['topology']['origin']['orientation']['y'])
        topology_.topology_orient.append(map_data['topology']['origin']['orientation']['z'])
        topology_.topology_orient.append(map_data['topology']['origin']['orientation']['w'])

    return jsonify(success=True)


@app.route('/save', methods=['POST'])
def save_to_file():

    data = request.get_json()

    if 'filePath' not in data:
        return jsonify(success=False, error='No filepath provided')
    
    filename = data['filePath']
    topology = {'Vertex': {}, 'Edge': {}}

    vertex_list = [vertex for vertex in topology_.vertices]
    edge_list = [edge for edge in topology_.edges]

    for idx, id in enumerate(vertex_list):
        topology['Vertex'][idx] = {}
        topology['Vertex'][idx]['id'] = topology_.vertices[id].id
        topology['Vertex'][idx]['x'] = topology_.vertices[id].x
        topology['Vertex'][idx]['y'] = topology_.vertices[id].y
        topology['Vertex'][idx]['enabled'] = True
        topology['Vertex'][idx]['frame_id'] = "map"
    
    count = 0
    for edge_src in edge_list:
        for edge in topology_.edges[edge_src]:
            topology['Edge'][count] = {}
            topology['Edge'][count]['src'] = edge.src
            topology['Edge'][count]['dst'] = edge.dst
            topology['Edge'][count]['type'] = edge.type
            topology['Edge'][count]['cost'] = edge.cost
            topology['Edge'][count]['enabled'] = True
            count += 1

    serialized_data = yaml.dump(topology)

    with open(filename, 'w') as file:
        file.write(serialized_data)

    return jsonify(success=True)

@app.route('/get_visualized_topology', methods=['GET'])
def get_visualized_topology():
    vertex_list = []
    for id in topology_.vertices:
        x_val = (topology_.vertices[id].x - topology_.map_origin[0])/topology_.resolution
        y_val = (topology_.vertices[id].y - topology_.map_origin[1])/topology_.resolution

        _, _, yaw = euler_from_quaternion(topology_.topology_orient[0],
                                    topology_.topology_orient[1],
                                    topology_.topology_orient[2],
                                    topology_.topology_orient[3])

        x_val_ = (x_val - topology_.topology_origin[0]) * math.cos(-yaw) - (y_val - topology_.topology_origin[1]) * math.sin(-yaw)
        y_val_ = (x_val - topology_.topology_origin[0]) * math.sin(-yaw) + (y_val - topology_.topology_origin[1]) * math.cos(-yaw)

        vertex_list.append({'id': topology_.vertices[id].id,
                            'x': x_val_,
                            'y': y_val_})
        
    edge_list = []
    for id in topology_.vertices:

        if id not in topology_.edges:
            continue

        edges = topology_.edges[id]

        for edge in edges:
            edge_list.append({'src': edge.src,
                              "dst": edge.dst,
                              'cost': edge.cost})

    return jsonify(vertices=vertex_list,
                   edges = edge_list)


@app.route('/print_vertex', methods=['GET'])
def print_vertices():
    vertex_list = ""
    print('Printing', len(topology_.vertices), 'vertices')
    for vertex in topology_.vertices:
        vertex_list = vertex_list + vertex + " "
    return jsonify(success=True, data=vertex_list)


@app.route('/print_edge', methods=['GET'])
def print_edges():
    print('Print edge list')
    edge_list = ""
    for src in topology_.edges:
        for edge in topology_.edges[src]:
            edge_list = edge_list + edge.src + "-" +edge.dst + " "

    return jsonify(success=True, data=edge_list)

@app.route('/update_vertex_position', methods=['POST'])
def update_vertex():

    data = request.get_json()
    print('Update vertex', data['id'])

    id = data['id']
    # Convert pixel to coordinate dx,dy
    dx = data['dx'] * topology_.resolution
    dy = data['dy'] * topology_.resolution

    _, _, yaw = euler_from_quaternion(topology_.topology_orient[0],
                                topology_.topology_orient[1],
                                topology_.topology_orient[2],
                                topology_.topology_orient[3])

    dx_ = dx * math.cos(yaw) - dy * math.sin(yaw)
    dy_ = dx * math.sin(yaw) + dy * math.cos(yaw)


    topology_.vertices[id] = topology_.vertices[id].update(dx_, dy_)
    return jsonify(success=True)


@app.route('/add_new_vertex', methods=['POST'])
def add_new_vertex():
    
    data = request.get_json()
    
    x = data['x']
    y = data['y']

    numbers = [int(id.split('_')[1]) for id in topology_.vertices]
    if not numbers:
        new_id = 'T_0'
    else:
        new_id = 'T_' + str(max(numbers)+1)

    x = x * topology_.resolution
    y = y * topology_.resolution

    _, _, yaw = euler_from_quaternion(topology_.topology_orient[0],
                                    topology_.topology_orient[1],
                                    topology_.topology_orient[2],
                                    topology_.topology_orient[3])

    x = x - topology_.topology_origin[0]
    y = y - topology_.topology_origin[1]

    x_ = x * math.cos(yaw) - y * math.sin(yaw)
    y_ = x * math.sin(yaw) + y * math.cos(yaw)


    x_ = x_ + topology_.map_origin[0]
    y_ = y_ + topology_.map_origin[1]

    print("Add new vertex {} at {},{}".format(new_id, x_, y_))

    topology_.vertices[new_id] = Vertex(id = new_id,
                                        x = x_,
                                        y = y_)

    return jsonify({'id': new_id})


@app.route('/add_new_edge', methods=['POST'])
def add_new_edge():

    data = request.get_json()
    
    src = data['src']
    dst = data['dst']
    cost = data['cost']
    type = data['type']

    if src in topology_.edges:
        topology_.edges[src].append(Edge(src = src,
                                         dst = dst,
                                         cost = cost,
                                         type = type))
    else:
        topology_.edges[src] = \
            [Edge(src = src,
                  dst = dst,
                  cost = cost,
                  type = type)]
        
    return jsonify(success=True)

@app.route('/connect_edges', methods=['POST'])
def connect_edges():

    data = request.get_json()
    
    idList = data['idList']
    type = data['type']

    for i in range(len(idList)-1):
        srcID = 'T_' + str(idList[i])
        dstID = 'T_' + str(idList[i+1])

        if srcID not in topology_.vertices or dstID not in topology_.vertices:
            continue

        cost = get_distance(topology_.vertices[srcID],
                            topology_.vertices[dstID])
        
        if srcID in topology_.edges:
            topology_.edges[srcID].append(Edge(src = srcID,
                                               dst = dstID,
                                               cost = cost,
                                               type = type))
        else:
            topology_.edges[srcID] = [Edge(src = srcID,
                                               dst = dstID,
                                               cost = cost,
                                               type = type)]
    return jsonify(success=True)



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
