document.addEventListener("DOMContentLoaded", () => {
    const showAllBtn = document.getElementById("showAllBtn");
    const dropdownContent = document.getElementById("dropdownContent");
  
    showAllBtn.addEventListener("click", (event) => {
      event.preventDefault(); // Prevent default link behavior
      dropdownContent.classList.toggle("show");
    });
  
    // Optional: Close the dropdown if clicked outside
    document.addEventListener("click", (event) => {
      if (!event.target.closest(".dropdown")) {
        dropdownContent.classList.remove("show");
      }
    });
  });
  
  