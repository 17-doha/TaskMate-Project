// taskmate/static/js/login.js
// Script to dynamic the Alerts

document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
      // Set a timeout to slide up and remove the alert
      setTimeout(() => {
        alert.classList.add('hide'); // Trigger the slide-up animation
      }, 1500); // Show alert for 1.5 seconds

      // Remove the alert element after the animation completes
      alert.addEventListener('animationend', () => {
        if (alert.classList.contains('hide')) {
          alert.remove();
        }
      });
    });
  });