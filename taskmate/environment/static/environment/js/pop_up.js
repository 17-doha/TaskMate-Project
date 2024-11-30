const loadTaskModalButton = document.getElementById('loadTaskModalButton');

// load the modal
loadTaskModalButton.addEventListener('click', function () {

    // Use the URL passed from the template
    fetch(taskCreateUrl) 
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load modal content.');
            }
            return response.text(); // Get the HTML content
        })
        .then(html => {
            // Remove any existing modal from the DOM to prevent duplicates(da 34an kan by7sl change lmkan almodel kl ma touch)
            const existingModal = document.getElementById('createTaskModal');
            if (existingModal) {
                console.log("Removing existing modal");
                existingModal.remove();
            }

            // Append the fetched modal content to the body
            document.body.insertAdjacentHTML('beforeend', html);

            // Initialize and show the modal using Bootstrap's modal API
            const modal = new bootstrap.Modal(document.getElementById('createTaskModal'));

            // Add the class that triggers the smooth transition
            const modalElement = document.getElementById('createTaskModal');
            modalElement.classList.add('show'); // Manually add class for custom transition

            // Initialize and show the modal
            modal.show();

            modalElement.addEventListener('hidden.bs.modal', function () {
                modalElement.remove(); // Clean up modal when it's closed
            });
        })
        .catch(error => {
            console.error('Error loading modal:', error);
        });
});
