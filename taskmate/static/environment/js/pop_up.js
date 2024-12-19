// Reusable function to show the modal
function showModal(modalId) {
    const modal = new bootstrap.Modal(document.getElementById(modalId));
    modal.show();
}

// Reusable function to remove the modal from the DOM
function removeModal(modalId) {
    const modalElement = document.getElementById(modalId);
    if (modalElement) {
        modalElement.remove(); 
    }
}


///////////////////////////////////// create task /////////////////////////////////////////

$(document).ready(function () {
    // Event listener for the "Add Task" button (to load the create task form)
    $('#loadTaskModalButton').click(function () {
        // Use the `taskCreateUrl` variable directly here
        $.ajax({
            url: taskCreateUrl,
            method: 'GET',
            success: function (data) {
                // Clear any existing content in the modal
                $('#createTaskModalContent').html('');

                // Insert the fetched content into the modal
                $('#createTaskModalContent').html(data);
                $('#env_id').val(environment_id);

                // Show the modal using Bootstrap
                showModal('createTaskModal');
            },
            error: function (_, status, error) {
                console.error('Error fetching task create form:', status, error);
                alert('Failed to load the create form. Please try again later.');
            }
        });
    });
});



/////////////////////////////////////////// Edit Task  //////////////////////////////////////////



const editTaskModal = $('<div class="modal fade" id="editTaskModal" tabindex="-1" aria-labelledby="editTaskModalLabel" aria-hidden="true"></div>');
$('body').append(editTaskModal);


editTaskModal.on('hidden.bs.modal', function () {
    console.log("Modal closed, removing it from the DOM");
    removeModal('editTaskModal'); // Clean up modal after it's closed
});

$(document).ready(function () {
    $('.edit-task-btn').click(function () {

        const taskId = $(this).data('task-id');
        const url = `/task/edit/${taskId}/`;

        // Send an AJAX request 
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

