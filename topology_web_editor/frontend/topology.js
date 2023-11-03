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