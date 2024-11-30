// Reusable function to show the modal
function showModal(modalId) {
    const modal = new bootstrap.Modal(document.getElementById(modalId));
    modal.show();
}

// Reusable function to remove the modal from the DOM
function removeModal(modalId) {
    const modalElement = document.getElementById(modalId);
    if (modalElement) {
        modalElement.remove(); // Clean up modal when it's closed
    }
}

// Function to handle loading task creation modal
const loadTaskModalButton = document.getElementById('loadTaskModalButton');

// Event listener to load the modal content dynamically
loadTaskModalButton.addEventListener('click', function () {
    console.log("Load task modal button clicked");

    // Fetch the modal content (task creation form)
    fetch(taskCreateUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load modal content.');
            }
            return response.text(); // Get the HTML content
        })
        .then(html => {
            console.log("HTML content received:", html);

            // Remove any existing modal to avoid duplicates
            removeModal('createTaskModal');

            // Append the fetched modal content to the body
            document.body.insertAdjacentHTML('beforeend', html);

            // Initialize and show the modal using Bootstrap's modal API
            showModal('createTaskModal');

            // Clean up the modal when it's closed
            const modalElement = document.getElementById('createTaskModal');
            modalElement.addEventListener('hidden.bs.modal', function () {
                console.log("Modal closed, removing it from the DOM");
                removeModal('createTaskModal'); // Clean up modal after it's closed
            });
        })
        .catch(error => {
            console.error('Error loading modal:', error);
            alert('An error occurred while loading the modal. Please try again.');
        });
});

/////////////////////////////////////////// Edit Task Pop Up //////////////////////////////////////////



// Create the modal element and append it to the DOM
const editTaskModal = $('<div class="modal fade" id="editTaskModal" tabindex="-1" aria-labelledby="editTaskModalLabel" aria-hidden="true"></div>');
$('body').append(editTaskModal);

// Set up the event listener for the modal's hidden event
editTaskModal.on('hidden.bs.modal', function () {
    console.log("Modal closed, removing it from the DOM");
    removeModal('editTaskModal'); // Clean up modal after it's closed
});

$(document).ready(function () {
    // Event listener for Edit Task buttons
    $('.edit-task-btn').click(function () {
        const taskId = $(this).data('task-id'); // Get task ID from button data attribute

        // Construct URL for fetching the edit form
        const url = `/task/edit/${taskId}/`;

        // Send an AJAX request to fetch the edit form for the task
        $.ajax({
            url: url,
            method: 'GET',
            success: function (data) {
                // Clear any existing content in the modal
                $('#editTaskModalContent').html('');

                // Insert the fetched content into the modal
                $('#editTaskModalContent').html(data);

                // Show the modal using Bootstrap
                showModal('editTaskModal');
            },
            error: function (_, status, error) {
                console.error('Error fetching task edit form:', status, error);
                alert('Failed to load the edit form. Please try again later.');
            }
        });
    });
});

