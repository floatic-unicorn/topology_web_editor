function handleTab(event, inputId) {
    var input = document.getElementById(inputId);

    if (event.key === "Tab") {
        event.preventDefault(); // Prevent the default tab behavior
        input.value = input.placeholder;
    }
}

function handleInput(event, inputId) {
    var input = document.getElementById(inputId);
    // Check if the input is empty, and if it is, set the placeholder
    if (!event.target.value.trim()) {
        input.value = input.placeholder;
    }
}