const symbolSelect = document.getElementById("symbolSelect");
      const limitSelect = document.getElementById("limitSelect");
      const ctx = document.getElementById("financeChart").getContext("2d");
      let chart;

      // Function to update the chart with new data
      function updateChart(data) {
        chart.data.labels.push(data["Open time"]);
        chart.data.datasets[0].data.push(parseFloat(data.Close));
        chart.data.datasets[1].data.push(parseFloat(data.Volume));

        // Check and remove the first data point if it exceeds the maximum limit
        if (chart.data.labels.length > getSelectedLimit()) {
          chart.data.labels.shift();
          chart.data.datasets[0].data.shift();
          chart.data.datasets[1].data.shift();
        }

        chart.update();
      }

      // Function to read the JSON file and update the chart
      async function readDataFile() {
        console.log("Reading data file...");
        try {
          const response = await fetch("multi_symbol.json");
          const lines = await response.text();
          const jsonData = lines
            .trim()
            .split("\n")
            .map((line) => JSON.parse(line));

          const selectedSymbol = symbolSelect.value;
          const newData = jsonData.filter((data) =>
            data.hasOwnProperty(selectedSymbol)
          );

          const selectedLimit = getSelectedLimit();
          chart.data.labels.length = 0;
          chart.data.datasets[0].data.length = 0;
          chart.data.datasets[1].data.length = 0;

          newData.slice(-selectedLimit).forEach((data) => {
            const selectedData = data[selectedSymbol];
            chart.data.labels.push(selectedData["Open time"]);
            chart.data.datasets[0].data.push(parseFloat(selectedData.Close));
            chart.data.datasets[1].data.push(parseFloat(selectedData.Volume));
          });

          chart.update();
        } catch (error) {
          console.error("Error reading data file:", error);
        }
      }

      // Function to read the selected symbol from localStorage
      function getSelectedSymbol() {
        return localStorage.getItem("selectedSymbol") || "BTCUSDT";
      }

      // Function to save the selected symbol to localStorage
      function saveSelectedSymbol(symbol) {
        localStorage.setItem("selectedSymbol", symbol);
      }

      // Function to read the selected limit from localStorage
      function getSelectedLimit() {
        return parseInt(localStorage.getItem("selectedLimit")) || 20;
      }

      // Function to save the selected limit to localStorage
      function saveSelectedLimit(limit) {
        localStorage.setItem("selectedLimit", limit);
      }

      // Function to set the selected option in the select element
      function setSelectedOption(selectElement, value) {
        selectElement.value = value;
      }

      // Event listener for symbol selection change
      symbolSelect.addEventListener("change", function () {
        const selectedSymbol = symbolSelect.value;
        saveSelectedSymbol(selectedSymbol);
        readDataFile();
      });

      // Event listener for limit selection change
      limitSelect.addEventListener("change", function () {
        const selectedLimit = limitSelect.value;
        saveSelectedLimit(selectedLimit);
        readDataFile();
      });

      // Initialize the chart
      chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: [],
          datasets: [
            {
              type: "line",
              label: "Price",
              data: [],
              backgroundColor: "rgba(255, 0, 0, 0.5)",
              borderColor: "rgba(255, 0, 0, 1)",
              borderWidth: 1,
              yAxisID: "price",
            },
            {
              type: "bar",
              label: "Volume",
              data: [],
              backgroundColor: "rgba(0, 123, 255, 0.5)",
              borderColor: "rgba(0, 123, 255, 1)",
              borderWidth: 1,
              yAxisID: "volume",
            },
          ],
        },
        options: {
          scales: {
            y: [
              {
                id: "price",
                type: "linear",
                position: "left",
                beginAtZero: true,
              },
              {
                id: "volume",
                type: "linear",
                position: "right",
                beginAtZero: true,
              },
            ],
          },
        },
      });

      // Read the selected symbol from localStorage and set the selected option initially
      const selectedSymbol = getSelectedSymbol();
      setSelectedOption(symbolSelect, selectedSymbol);

      // Read the selected limit from localStorage and set the selected option initially
      const selectedLimit = getSelectedLimit();
      setSelectedOption(limitSelect, selectedLimit.toString());

      // Read the JSON file and update the chart initially
      readDataFile();