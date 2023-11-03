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
                statusDiv.textContent = 'Topology loaded successfully!';
            } else {
                statusDiv.textContent = 'Error loading YAML file.';
            }
        })
        .catch(error => {
            statusDiv.textContent = 'Error loading YAML file.';
        });
    }

    alert(statusDiv.textContent);
}
