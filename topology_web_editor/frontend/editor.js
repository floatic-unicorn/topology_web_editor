function loadMarkers(vertices) {
    const markerContainer = document.getElementById('markerContainer');
    const image = document.querySelector('img[src="map.png"][alt="Navigation Map"]');
    const imageRect = image.getBoundingClientRect();
    const imageX = imageRect.left;
    const imageY = imageRect.top;

    vertices.forEach(vertex => {
        const marker = document.createElement('div');
        marker.className = 'marker';
        marker.id = vertex.id;
        const xOnImage = -imageX + vertex.x;
        const yOnImage = -imageY + vertex.y;
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

                    updateVertexPosition(target);
                }
            });

        markerContainer.appendChild(marker);
    });
}

// Create function to send vertex position (pixel coordinates) updates to server
function updateVertexPosition(marker) {
    const x = parseFloat(marker.style.left) || 0;
    const y = parseFloat(marker.style.top) || 0;
    const image = document.querySelector('img[src="map.png"][alt="Navigation Map"][id="mapImage"]');
    const imageRect = image.getBoundingClientRect();
    const imageX = imageRect.left;
    const imageY = imageRect.top;

    marker.className = 'marker';
    const xOnMap = x + imageX;
    const yOnMap = y + imageY;

    const requestData = {
        'id': marker.id,  // You can add an id to each marker for identification
        'x': xOnMap,
        'y': yOnMap,
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