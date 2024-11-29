// Ensure the button ID matches the one in your environment template
const loadTaskModalButton = document.getElementById('loadTaskModalButton');

// Add an event listener to load the modal
loadTaskModalButton.addEventListener('click', function () {
    console.log("Load task modal button clicked");

    // Use the URL passed from the template
    fetch(taskCreateUrl) 
        .then(response => {
            console.log("Modal content fetched");
            if (!response.ok) {
                throw new Error('Failed to load modal content.');
            }
            return response.text(); // Get the HTML content
        })
        .then(html => {
            console.log("HTML content received:", html);

            // Remove any existing modal from the DOM to prevent duplicates
            const existingModal = document.getElementById('createTaskModal');
            if (existingModal) {
                console.log("Removing existing modal");
                existingModal.remove();
            }

            // Append the fetched modal content to the body
            console.log("Appending new modal content");
            document.body.insertAdjacentHTML('beforeend', html);

            // Initialize and show the modal using Bootstrap's modal API
            const modal = new bootstrap.Modal(document.getElementById('createTaskModal'));
            console.log("Initializing modal");

            // Add the class that triggers the smooth transition
            const modalElement = document.getElementById('createTaskModal');
            modalElement.classList.add('show'); // Manually add class for custom transition

            // Initialize and show the modal
            modal.show();

            // Optional: Add any additional event listeners for the modal
            modalElement.addEventListener('hidden.bs.modal', function () {
                console.log("Modal closed, removing it from the DOM");
                modalElement.remove(); // Clean up modal when it's closed
            });
        })
        .catch(error => {
            console.error('Error loading modal:', error);
        });
});
