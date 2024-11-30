const searchInput = document.getElementById('searchInput');
const searchForm = document.getElementById('searchForm');

searchInput.addEventListener('keydown', function(event) {
  if (event.key === 'Enter') {
    searchForm.submit();
  }
});

const searchBtn = document.querySelector('.search-btn');
searchBtn.addEventListener('click', function(event) {
  event.preventDefault();
  searchForm.submit();
});

function updateActionUrl() {
  const searchInput = document.getElementById('searchInput').value.trim().toLowerCase();
  const form = document.getElementById('searchForm');

  if (searchInput.includes("task") || !isNaN(searchInput)) {
    form.action = "{% url 'task:search_task' %}";
  } else {
    form.action = "{% url 'environment:search_environment' %}";
  }
}
