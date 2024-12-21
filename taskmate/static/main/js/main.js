const labels = environmentStats.map(stat => stat.environment_id__label || "No Environment");
const progressData = environmentStats.map(stat => (stat.done_ratio * 100).toFixed(2)); 

if (environmentStats.length === 0 || (environmentStats.length > 0 && environmentStats[0]['done_tasks'] === 0)) {
  console.error("No data available for chart.");
  document.getElementById("chart-title").style.display = "none";
} else {

  let ctx = document.getElementById("chart").getContext("2d");
  let chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Progress %",
          backgroundColor: "#a18dfb",
          borderColor: "#e0e0e0",
          data: progressData
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: "y",
      plugins: {
        legend: { display: false }, 
        tooltip: { enabled: true }
      },
      scales: {
        x: {
          grid: { display: false },
          display: false
        },
        y: {
          grid: { display: false },
          display: true
        }
      }
    }
  });
}