/* Click and add */
function addSingleVertex() {

    document.getElementById('imageContainer').addEventListener('click', function (event) {
        if (event.target.id === 'mapImage') {
            const x = event.clientX;
            const y = event.clientY;

            /* Add to topology and get ID as response */
            const image = event.target.getBoundingClientRect();
            const relX = x - image.left;
            const relY = image.bottom - y;

            addVertex(relX, relY);
        }
    });
}

/* Right-click drag and add */
function addMultipleVertices(interval_in_pixels) {
    const imageContainer = document.getElementById('imageContainer');

    let startX, startY;

    imageContainer.addEventListener('contextmenu', function (event) {
        event.preventDefault();
    });

    imageContainer.addEventListener('mousedown', function (event) {
        event.preventDefault();

        if (event.button === 2 && event.target.id === 'mapImage') {
            console.log('Right-clicked on mapImage');

            startX = event.clientX;
            startY = event.clientY;

            const image = event.target.getBoundingClientRect();

            const relX = startX - image.left;
            const relY = image.bottom - startY;
            addVertex(relX, relY);

            const handleMove = async function (moveEvent) {
                moveEvent.preventDefault();

                const currentX = moveEvent.clientX;
                const currentY = moveEvent.clientY;

                const deltaX = currentX - startX;
                const deltaY = currentY - startY;
                const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);

                if (distance > interval_in_pixels) {
                    // Add the dot to topology and get ID as a response
                    const relX = currentX - image.left;
                    const relY = image.bottom - currentY;

                    startX = currentX;
                    startY = currentY;

                    addVertex(relX, relY);
                }
            };

            const handleRelease = function () {
                console.log('Right-click released on mapImage');
                document.removeEventListener('mousemove', handleMove);
                document.removeEventListener('mouseup', handleRelease);
            };

            document.addEventListener('mousemove', handleMove);
            document.addEventListener('mouseup', handleRelease);
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
            }
        });

    markerContainer.appendChild(marker);
}
