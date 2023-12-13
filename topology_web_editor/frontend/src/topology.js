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
            console.log('Marker position updated successfully.');
        } else {
            console.error('Error updating marker position.');
        }
    })
    .catch(error => {
        console.error('Error updating marker position.');
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
            statusDiv.textContent = 'Vertex removed successfully!';
        } else {
            statusDiv.textContent = 'Error removing vertex.';
        }
    })
    .catch(error => {
        statusDiv.textContent = 'Error loading remove vertex';
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
            statusDiv.textContent = 'Add edge successfully!';
        } else {
            statusDiv.textContent = 'Error adding edge.';
        }
    })
    .catch(error => {
        statusDiv.textContent = 'Error loading add edge';
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
            statusDiv.textContent = 'Connected edges successfully!';
        } else {
            statusDiv.textContent = 'Error connecting edge.';
        }
    })
    .catch(error => {
        statusDiv.textContent = 'Error loading connect edges';
    });
}
