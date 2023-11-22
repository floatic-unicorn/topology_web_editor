function loadMarkers(vertices) {
    const markerContainer = document.getElementById('markerContainer');
    const imageRect = markerContainer.getBoundingClientRect();
    const imageLeft = imageRect.left;
    const imageBottom = imageRect.bottom;

    vertices.forEach(vertex => {
        const marker = document.createElement('div');
        marker.className = 'marker';
        marker.id = vertex.id;
        const xOnImage = vertex.x;
        const yOnImage = vertex.y;
        marker.style.left = xOnImage + 'px';
        marker.style.bottom = yOnImage + 'px';

        // Make the marker draggable using interact.js
        interact(marker)
            .draggable({
                onmove: (event) => {
                    const target = event.target;
                    const x = (parseFloat(target.style.left)) + event.dx;
                    const y = (parseFloat(target.style.bottom)) - event.dy;

                    target.style.left = x + 'px';
                    target.style.bottom = y + 'px';

                    updateVertexPosition(target, event.dx, event.dy);
                }
            });

        markerContainer.appendChild(marker);
    });
}

// Create function to send vertex position (pixel coordinates) updates to server
function updateVertexPosition(marker, dx, dy) {

    const requestData = {
        'id': marker.id,  // You can add an id to each marker for identification
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