// Create the initial line chart
const ctx = document.getElementById("financeChart").getContext("2d");
const chart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [],
    datasets: [
      {
        label: "Price",
        data: [],
        backgroundColor: "rgba(0, 123, 255, 0.5)",
        borderColor: "rgba(0, 123, 255, 1)",
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: false,
      },
    },
  },
});

// Function to update the chart with new data
function updateChart(data) {
  chart.data.labels.push(data.time);
  chart.data.datasets[0].data.push(data.total);
  chart.update();
}

// Function to read the JSON file and update the chart
async function readDataFile() {
  console.log("Reading data file...");
  try {
    const response = await fetch("account_balance.json");
    const lines = await response.text();
    const jsonData = lines
      .trim()
      .split("\n")
      .map((line) => JSON.parse(line));

    // Filter out duplicates
    const existingLabels = chart.data.labels;
    const newData = jsonData.filter(
      (data) => !existingLabels.includes(data.time)
    );

    // Update the chart with non-duplicate data
    newData.forEach((data) => updateChart(data));
    applyCustomRange();
  } catch (error) {}
}

// Function to continuously update the chart at a specified interval
function startUpdatingChart(interval) {
  setInterval(function () {
    readDataFile();
  }, interval);
}

// Event listener for the select button
const limitSelect = document.getElementById("limitSelect");
limitSelect.addEventListener("change", function () {
  const selectedLimit = parseInt(limitSelect.value);
  updateChartLimit(selectedLimit);
  // Save the selected value to localStorage
  localStorage.setItem("selectedLimit", selectedLimit);
});

// Function to update the chart with the selected limit
function updateChartLimit(limit) {
  if (chart.data.labels.length > limit) {
    const difference = chart.data.labels.length - limit;
    chart.data.labels.splice(0, difference);
    chart.data.datasets[0].data.splice(0, difference);
    chart.update();
  }
}

// Read the JSON file and update the chart initially
readDataFile();

// Retrieve the selected value from localStorage and set it as the initial selected value
const savedSelectedLimit = localStorage.getItem("selectedLimit");
if (savedSelectedLimit) {
  limitSelect.value = savedSelectedLimit;
  updateChartLimit(parseInt(savedSelectedLimit));
}

// Start updating the chart every 30 seconds (30000 milliseconds)
// startUpdatingChart(30000);