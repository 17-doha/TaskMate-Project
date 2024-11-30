/**
 * Allows an element to be a valid drop target by preventing the default behavior.
 * 
 * @param {Event} ev - The event object representing the drag event.
 */
function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

/**
 * Handles the drop event by appending the dropped task to the target column.
 * It also makes a POST request to update the task's table ID in the database.
 * 
 * @param {Event} ev - The event object representing the drop event.
 */

function drop(ev) {   

    ev.preventDefault();

    const column = ev.target.closest('.column');
    
    // Check if the drop target is indeed a column (not a task)
    if (!column || ev.target.classList.contains('task-card')) {
        return; // Prevent dropping inside another task
    }

    // Find the "No tasks" message inside this column and remove it
    const noTasksMessage = column.querySelector('.no-tasks-message');
    if (noTasksMessage) {
        noTasksMessage.remove(); 
    }

    var data = ev.dataTransfer.getData("text");
    var task = document.getElementById(data);
    ev.target.appendChild(task);
    var taskId = task.getAttribute('data-task-id');
    var targetColumn = ev.target.closest('.column');
    var targetTableName = targetColumn.querySelector('h3').textContent;

    // Make a POST request to update the task's table ID
    fetch(`/environment/${environment_id}/drag-and-drop/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({
            'task_id': taskId,
            'target_table': targetTableName
        })
    })
    .then(response => response.json())

}
