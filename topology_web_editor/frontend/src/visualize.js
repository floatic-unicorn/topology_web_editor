function drawTopology(vertices, edges) {
    const markerContainer = document.getElementById('markerContainer');

    vertices.forEach(vertex => {
        const marker = document.createElement('div');
        marker.className = 'marker';
        marker.id = vertex.id;
        const xOnImage = vertex.x;
        const yOnImage = vertex.y;
        marker.style.left = xOnImage + 'px';
        marker.style.bottom = yOnImage + 'px';

        const idLabel = document.createElement('div');
        idLabel.className = 'marker-id';
        idLabel.textContent = vertex.id;

        marker.appendChild(idLabel);

        // Make marker removable via right-click
        marker.addEventListener('contextmenu', function(event) {
            // Prevent the default context menu from showing
            event.preventDefault();

            // Create a "Remove" button
            const removeButton = document.createElement('button');
            removeButton.textContent = 'Remove';
            removeButton.addEventListener('click', function () {
                // Remove the marker when the "Remove" button is clicked
                markerContainer.removeChild(marker);
                removeVertex(marker.id);
                drawEdges_(edges);
            });

            marker.appendChild(removeButton);
        });

        // Make the marker draggable using interact.js
        interact(marker)
            .draggable({
                onmove: (event) => {
                    const target = event.target;
                    const x = (parseFloat(target.style.left)) + event.dx;
                    const y = (parseFloat(target.style.bottom)) - event.dy;

                    target.style.left = x + 'px';
                    target.style.bottom = y + 'px';

                    updateVertex(target.id, event.dx, -event.dy);
                    drawEdges_(edges);
                }
            });

        markerContainer.appendChild(marker);
    });

    // Visualize edges
    drawEdges_(edges);
}


function drawEdges() {

    fetch('http://127.0.0.1:5000/get_visualized_edges', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        const edges = data.edges;
        drawEdges_(edges);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function drawEdges_(edges) {

    // Visualize edges
    const edgeCanvas = document.getElementById('visualizedEdges');
    const ctx = edgeCanvas.getContext('2d');
    ctx.clearRect(0, 0, edgeCanvas.width, edgeCanvas.height);

    // Iterate over edges and draw arrows
    edges.forEach(edge => {
        const srcMarker = document.getElementById(edge.src);
        const dstMarker = document.getElementById(edge.dst);

        if (srcMarker && dstMarker) {
            // Drawing logic for the arrow
            drawArrow(ctx, srcMarker, dstMarker);
        }
    });
}

function drawArrow(ctx, srcMarker, dstMarker) {
    // Code to draw an arrow between two points
    // (You can customize the appearance of the arrow)
    const startX = parseFloat(srcMarker.style.left);
    const startY = ctx.canvas.height - parseFloat(srcMarker.style.bottom);
    const endX = parseFloat(dstMarker.style.left);
    const endY = ctx.canvas.height - parseFloat(dstMarker.style.bottom);


    ctx.beginPath();
    ctx.moveTo(startX, startY);
    ctx.lineTo(endX, endY);
    ctx.strokeStyle = "rgb(255, 178, 102)";
    ctx.lineWidth = 1.8;

    const arrowSize = 7;
    const angle = Math.atan2(endY - startY, endX - startX);
    ctx.lineTo(endX - arrowSize * Math.cos(angle - Math.PI / 6), endY - arrowSize * Math.sin(angle - Math.PI / 6));
    ctx.moveTo(endX, endY);
    ctx.lineTo(endX - arrowSize * Math.cos(angle + Math.PI / 6), endY - arrowSize * Math.sin(angle + Math.PI / 6));

    ctx.stroke();
    ctx.closePath();
}