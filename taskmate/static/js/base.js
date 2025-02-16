document.addEventListener("DOMContentLoaded", () => {
    const toggleIcon = document.querySelector(".theme-toggle-icon");
  
    // Check for saved theme preference
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
      document.body.classList.add("dark-mode");
    }
  
    toggleIcon.addEventListener("click", () => {
      document.body.classList.toggle("dark-mode");
  
      // Save the user's preference to localStorage
      if (document.body.classList.contains("dark-mode")) {
        localStorage.setItem("theme", "dark");
      } else {
        localStorage.setItem("theme", "light");
      }
    });
  });

// Select the theme toggle button
const themeToggleButton = document.querySelector('.theme-toggle-icon');

// Add an event listener to the button
themeToggleButton.addEventListener('click', () => {
  // Toggle the dark-mode class on the body
  document.body.classList.toggle('dark-mode');
});
