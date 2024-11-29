
function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    var task = document.getElementById(data);
    ev.target.appendChild(task);
    var taskId = task.getAttribute('data-task-id');
    var targetColumn = ev.target.closest('.column');
    var targetTableName = targetColumn.querySelector('h3').textContent;

    // Make a POST request to update the task's table ID
    fetch(`/environment/1/drag-and-drop/`, {
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