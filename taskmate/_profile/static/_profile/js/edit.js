document.getElementById('editBtn').addEventListener('click', function() {
    const inputs = document.querySelectorAll('input[readonly]');
    inputs.forEach(input => {
        input.removeAttribute('readonly');
        input.style.cursor = 'text'; // Make cursor a text input when editable
    });
    document.getElementById('saveBtn').style.display = 'inline-block'; // Show save button
    this.style.display = 'none'; // Hide edit button
});

document.getElementById('UserprofileForm').addEventListener('submit', function(event) {
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.setAttribute('readonly', true); // Set all inputs back to readonly after save
        input.style.cursor = 'not-allowed'; // Change cursor to not-allowed on readonly
    });
    document.getElementById('saveBtn').style.display = 'none'; // Hide save button
    document.getElementById('editBtn').style.display = 'inline-block'; // Show edit button
});