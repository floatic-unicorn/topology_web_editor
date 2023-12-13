function addVertex(x, y) {

    const requestData = {
        'x': x,
        'y': y,
      };

    fetch('http://127.0.0.1:5000/add_new_vertex', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(requestData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            console.log(`New vertex created successfully with ID: ${data.id}`);
            addMarker(x, y, data.id);
        } else {
            console.error('Error creating a new vertex.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function updateVertex(id, dx, dy) {

    const requestData = {
        'id': id,
        'dx': dx,
        'dy': dy,
    };

    fetch('http://127.0.0.1:5000/update_vertex_position', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Vertex position updated successfully.');
        } else {
            console.error('Error updating vertex position.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function removeVertex(id) {

    const requestData = {'id': id };

    fetch('http://127.0.0.1:5000/remove_vertex', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Vertex removed successfully!');
        } else {
            console.error('Error removing vertex.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function addEdge() {
    const edge = document.getElementById('newEdge').value.split(",");
    const src = edge[0];
    const dst = edge[1];
    const cost = edge[2];
    const type = edge[3];

    const requestData = {'src': src,
                         'dst': dst,
                         'cost' : cost,
                         'type' : type                  
                        };

    fetch('http://127.0.0.1:5000/add_new_edge', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Added edges successfully!');
            // Update visualization
            drawEdges();
        } else {
            console.log('Error adding edge.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });

}

function connectEdges() {
    const inputValue = document.getElementById('connectEdges').value;

    var match = inputValue.match(/^\[(.*?)\],(.*)$/);

    if (match) {
        var idList = match[1].split(',').map(Number);
        var type = match[2];

        console.log('ID List:', idList);
        console.log('Type:', type);
    } else {
        console.error('Invalid input format. Please enter in the format "[3,1,5],rack".');
    }

    const requestData = {'idList': idList,
                         'type' : type                  
                        };

    fetch('http://127.0.0.1:5000/connect_edges', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Connected edges successfully!');
            // Update visualization
            drawEdges();
        } else {
            console.log('Error connecting edge.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function get_topology() {

    fetch('http://127.0.0.1:5000/get_visualized_topology', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        const vertices = data.vertices;
        const edges = data.edges;
    })
    .catch(error => {
        console.error('Error:', error);
    });

    return vertices, edges;
}

function get_vertices() {

    fetch('http://127.0.0.1:5000/get_visualized_vertices', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        const vertices = data.vertices;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function get_edges() {

    fetch('http://127.0.0.1:5000/get_visualized_edges', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        const edges = data.edges;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}