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

function deleteMarker() {
    
}