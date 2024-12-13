// Get the modal and buttons
var modal = document.getElementById("confirmationModal");
var deleteBtn = document.getElementById("deleteBtn");
var closeBtn = document.getElementById("closeBtn");
var cancelBtn = document.getElementById("cancelBtn");
var confirmBtn = document.getElementById("confirmBtn");

// When the delete button is clicked, show the modal
deleteBtn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on the close button (x), hide the modal
closeBtn.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks on "Cancel", hide the modal
cancelBtn.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks on "Yes, Delete", perform the deletion action
confirmBtn.onclick = function() {
  // Perform your delete action here
  alert("Item Deleted!");
  modal.style.display = "none"; // Close the modal
}

// When the user clicks anywhere outside the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}