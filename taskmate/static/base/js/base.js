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