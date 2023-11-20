from flask import Flask, request, jsonify
from flask_cors import CORS
import yaml
from topology import Topology, Vertex, Edge

app = Flask(__name__)
CORS(app)

topology_ = Topology()


@app.route('/load', methods=['POST'])
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

@app.route('/get_vertex_pixels', methods=['GET'])
def get_vertices():
    vertex_list = []
    for id in topology_.vertices:
        vertex_list.append({'id': topology_.vertices[id].id,
                            'x': int(topology_.vertices[id].x-topology_.origin[0])/topology_.resolution,
                            'y': int(topology_.vertices[id].y-topology_.origin[1])/topology_.resolution})
    return jsonify(vertices=vertex_list)


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
    dx = data['dx']*topology_.resolution
    dy = data['dy']*topology_.resolution

    topology_.vertices[id] = topology_.vertices[id].update(dx, dy)
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)