function saveToFile() {
    const fileOutput = document.getElementById('outputFile');
    const statusDiv = document.getElementById('status');

    const filename = fileOutput.value;
    alert("Save data to " + filename);

    if (filename) {
        const requestData = { 'filePath': filename };

        fetch('http://127.0.0.1:5000/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                statusDiv.textContent = 'Topology saved successfully!';
            } else {
                statusDiv.textContent = 'Error writing to YAML file.';
            }
        })
        .catch(error => {
            statusDiv.textContent = 'Error writing to YAML file.';
        });
    }
}

function loadFromFile() {

    const fileInput = document.getElementById('inputFile');
    const statusDiv = document.getElementById('status');
    const markerContainer = document.getElementById('markerContainer');  // Reference to the marker container


    const filename = fileInput.value;
    alert("Requested data from " + filename);

    if (filename) {
        const requestData = { 'filePath': filename };

        fetch('http://127.0.0.1:5000/load', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Fetch vertices and create markers after topology is loaded
                fetch('http://127.0.0.1:5000/get_vertex_pixels', {
                    method: 'GET'
                })
                .then(response => response.json())
                .then(data => {
                    const vertices = data.vertices;

                    const image = document.querySelector('img[src="map.png"][alt="Navigation Map"]');
                    const imageRect = image.getBoundingClientRect();
                    const imageX = imageRect.left;
                    const imageY = imageRect.top;

                    vertices.forEach(vertex => {
                        const marker = document.createElement('div');
                        marker.className = 'marker';
                        const xOnImage = -imageX - 300+ vertex.x;
                        const yOnImage = -imageY + 150 + vertex.y;
                        marker.style.left = xOnImage + 'px';
                        marker.style.top = yOnImage + 'px';

                        // Make the marker draggable using interact.js
                        interact(marker)
                            .draggable({
                                onmove: (event) => {
                                    const target = event.target;
                                    const x = (parseFloat(target.style.left) || 0) + event.dx;
                                    const y = (parseFloat(target.style.top) || 0) + event.dy;

                                    target.style.left = x + 'px';
                                    target.style.top = y + 'px';
                                }
                            });

                        markerContainer.appendChild(marker);
                    });
                })
                .catch(error => {
                    alert('Error loading topology markers.');
                });
            } else {
                alert('Error loading YAML file.');
            }
        })
        .catch(error => {
            alert('Error loading YAML file.');
        });
    }
}

function printTopology() {

    var message = "Print topology";
    alert(message);

    fetch('http://127.0.0.1:5000/print_vertex', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            statusDiv.textContent = 'Topology loaded successfully!';
        } else {
            statusDiv.textContent = 'Error loading YAML file.';
        }
    })
    .catch(error => {
        statusDiv.textContent = 'Error loading YAML file.';
    });

    fetch('http://127.0.0.1:5000/print_edge', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            statusDiv.textContent = 'Topology loaded successfully!';
        } else {
            statusDiv.textContent = 'Error loading YAML file.';
        }
    })
    .catch(error => {
        statusDiv.textContent = 'Error loading YAML file.';
    });
}