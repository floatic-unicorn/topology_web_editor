from flask import Flask, request, jsonify
from flask_cors import CORS
import yaml
import math

from model.topology import Topology, Vertex, Edge
from utils.geometry import euler_from_quaternion, get_distance
from utils.topology import *

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
    
    copy_topology_data_from_yaml(topology, topology_)

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

    copy_map_data_from_yaml(map_data, topology_)

    return jsonify(success=True)


@app.route('/save', methods=['POST'])
def save_to_file():

    data = request.get_json()

    if 'filePath' not in data:
        return jsonify(success=False, error='No filepath provided')
    
    filename = data['filePath']
    topology = {'Vertex': {}, 'Edge': {}}

    convert_topology_to_yaml(topology_, topology)

    serialized_data = yaml.dump(topology)

    with open(filename, 'w') as file:
        file.write(serialized_data)

    return jsonify(success=True)


@app.route('/get_visualized_topology', methods=['GET'])
def get_visualized_topology():

    vertex_list, edge_list = get_raw_topology(topology_)

    return jsonify(vertices=vertex_list,
                   edges = edge_list)


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
