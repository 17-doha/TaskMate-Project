$(document).ready(function () {
    // When the Edit Task button is clicked
    $('.edit-task-btn').click(function () {
        // Get the task ID from the button's data-task-id attribute
        var taskId = $(this).data('task-id');

        // Construct the URL for the AJAX request
        var url = '/task/edit/' + taskId + '/';  

        // Send the AJAX request to fetch the edit form for this task
        $.ajax({
            url: url,  
            method: 'GET',
            success: function (data) {
                // Insert the fetched form into the modal content
                $('#editTaskModalContent').html(data);

                // Show the modal (Bootstrap method)
                $('#editTaskModal').modal('show');
            },
            error: function (_, status, error) {
                console.error("Error fetching task edit form:", status, error);
                alert("Failed to load the edit form. Please try again.");
            }
        });
    });
});
