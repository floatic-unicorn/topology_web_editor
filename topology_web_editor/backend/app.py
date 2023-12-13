from flask import Flask, request, jsonify
from flask_cors import CORS
import yaml

from model.topology import Topology
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
            return jsonify(success=True)
    
    topology_.clear_topology_data()
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
            return jsonify(success=True)

    topology_.clear_map_data()
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


@app.route('/get_visualized_vertices', methods=['GET'])
def get_visualized_vertices():
    vertex_list = get_raw_vertices(topology_)
    
    return jsonify(vertices = vertex_list) 


@app.route('/get_visualized_edges', methods=['GET'])
def get_visualized_edges():

    edge_list = get_raw_edges(topology_)
    
    return jsonify(edges = edge_list) 


@app.route('/update_vertex_position', methods=['POST'])
def update_vertex_position():

    data = request.get_json()
    print('Update vertex', data['id'])

    id = data['id']
    # Convert pixel to coordinate dx,dy
    dx = data['dx'] * topology_.resolution
    dy = data['dy'] * topology_.resolution

    update_vertex(topology_, id, dx, dy)

    return jsonify(success=True)


@app.route('/add_new_vertex', methods=['POST'])
def add_new_vertex():
    
    data = request.get_json()
    
    x = data['x']
    y = data['y']
    
    new_id = add_vertex(topology_, x, y)

    return jsonify({'id': new_id})


@app.route('/add_new_edge', methods=['POST'])
def add_new_edge():

    data = request.get_json()
    
    src = data['src']
    dst = data['dst']
    cost = data['cost']
    type = data['type']

    add_edge(topology_, src, dst, cost, type)
        
    return jsonify(success=True)

@app.route('/remove_vertex', methods=['POST'])
def remove_vertex_with_edges():

    data = request.get_json()

    remove_vertex(topology_, data['id'])

    return jsonify(success=True)

@app.route('/connect_edges', methods=['POST'])
def connect_new_edges():

    data = request.get_json()
    
    idList = data['idList']
    type = data['type']

    connect_edges(topology_, idList, type)

    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
