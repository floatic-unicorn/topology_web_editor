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
                console.log('Topology saved successfully!');
            } else {
                console.log('Error writing to YAML file.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

function loadTopologyFromFile() {
    const fileInput = document.getElementById('inputFile');
    const statusDiv = document.getElementById('status');
    const filename = fileInput.value;

    alert("Requested data from " + filename);

    if (filename) {
        const requestData = { 'filePath': filename };

        fetch('http://127.0.0.1:5000/load_topology', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                fetch('http://127.0.0.1:5000/get_visualized_topology', {
                    method: 'GET'
                })
                .then(response => response.json())
                .then(data => {
                    const vertices = data.vertices;
                    const edges = data.edges;
                    console.log('Topology data loaded successfully!');
                    drawTopology(vertices, edges);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            } else {
                alert('Error loading YAML file.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

function loadMapFromFile() {
    const fileInput = document.getElementById('dataFile');
    const statusDiv = document.getElementById('status');
    const filename = fileInput.value;

    alert("Requested data from " + filename);

    if (filename) {
        const requestData = { 'filePath': filename };

        fetch('http://127.0.0.1:5000/load_map_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Map data loaded successfully!');
            } else {
                console.log('Error loading YAML file.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}
