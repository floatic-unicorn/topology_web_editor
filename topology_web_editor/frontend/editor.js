// Create function to send vertex position (pixel coordinates) updates to server
function updateVertexPosition(marker, dx, dy) {

    const requestData = {
        'id': marker.id,
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

function addNewVertex() {

    document.getElementById('imageContainer').addEventListener('click', function (event) {
        if (event.target.id === 'mapImage') {
          const x = event.clientX;
          const y = event.clientY;

          /* Add to topology and get ID as response */
          const image = event.target.getBoundingClientRect();
          const relX = x - image.left;
          const relY = image.bottom - y;

          const requestData = {
            'x': relX,
            'y': relY,
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
                    addMarker(relX, relY, data.id);
                } else {
                    console.error('Error creating a new vertex.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });
}

function addMarker(x, y, id) {

    const markerContainer = document.getElementById('markerContainer');

    const marker = document.createElement('div');
    marker.className = 'marker';
    marker.id = id;
    marker.style.left = x + 'px';
    marker.style.bottom = y + 'px';

    const idLabel = document.createElement('div');
    idLabel.className = 'marker-id';
    idLabel.textContent = id;

    marker.appendChild(idLabel);

    // Make the marker draggable using interact.js
    interact(marker)
        .draggable({
            onmove: (event) => {
                const target = event.target;
                const x = (parseFloat(target.style.left)) + event.dx;
                const y = (parseFloat(target.style.bottom)) - event.dy;

                target.style.left = x + 'px';
                target.style.bottom = y + 'px';

                updateVertexPosition(target, event.dx, -event.dy);
            }
        });

    markerContainer.appendChild(marker);
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