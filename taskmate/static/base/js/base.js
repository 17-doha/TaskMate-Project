// Dropdown toggle functionality
const dropdownMenu = document.querySelector('.menu-item.dropdown');
const submenu = dropdownMenu.querySelector('.submenu');

dropdownMenu.addEventListener('click', function (event) {
  event.stopPropagation(); // Prevent click from bubbling up
  const isOpen = dropdownMenu.classList.contains('open');

  // Close all other dropdowns (optional, if there are multiple dropdowns)
  document.querySelectorAll('.menu-item.dropdown').forEach(item => {
    item.classList.remove('open');
    item.querySelector('.submenu').style.display = 'none';
  });

  // Toggle the current dropdown
  if (!isOpen) {
    dropdownMenu.classList.add('open');
    submenu.style.display = 'block';
  } else {
    dropdownMenu.classList.remove('open');
    submenu.style.display = 'none';
  }
});

// Close dropdown if clicked outside
document.addEventListener('click', function () {
  dropdownMenu.classList.remove('open');
  submenu.style.display = 'none';
});

document.getElementById('add-environment-form').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent the form from submitting traditionally

  const form = event.target;
  const formData = new FormData(form);

  // Button and message elements
  const addBtn = document.getElementById('add-btn');
  const messageContainer = document.getElementById('modal-message');

  // Show loading spinner on the button
  addBtn.innerHTML = '<span class="spinner"></span> Adding...';
  addBtn.disabled = true;

  fetch(form.action, {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
    }
  })
    .then(response => response.json())
    .then(data => {
      addBtn.innerHTML = 'Add'; // Reset button text
      addBtn.disabled = false;

      if (data.success) {
        closeAddEnvironmentModal(); // Close modal immediately
        alert(data.message); // Optional: Show an alert
      } else {
        messageContainer.style.display = 'block';
        messageContainer.className = 'error';
        messageContainer.textContent = data.error;
      }
    })
    .catch(error => {
      addBtn.innerHTML = 'Add'; // Reset button text
      addBtn.disabled = false;

      messageContainer.style.display = 'block';
      messageContainer.className = 'error';
      messageContainer.textContent = 'An unexpected error occurred. Please try again.';
    });
});

function closeAddEnvironmentModal() {
  const modal = document.getElementById('add-environment-modal');
  modal.style.display = 'none';
}

function openAddEnvironmentModal() {
  const modal = document.getElementById('add-environment-modal');
  modal.style.display = 'flex';
}