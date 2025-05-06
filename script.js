document.addEventListener("DOMContentLoaded", function () {
    const algorithmSelect = document.getElementById("scheduling-algorithms");
    const processInputDiv = document.getElementById("process-input");
    const processTableBody = document.querySelector("#process-table tbody");
    const calculateButton = document.getElementById("calculate");
    const resultsDiv = document.getElementById("results");
    const addProcessButton = document.getElementById("add-process");
    // Show process input when an algorithm is selected
    algorithmSelect.addEventListener("change", function () {
        processInputDiv.style.display = "block";
    });
    // Add process row when Add Process button is clicked
    addProcessButton.addEventListener("click", function () {
        const newRow = document.createElement("tr");
        newRow.innerHTML = `
        <td><input type="text" class="process-id" /></td>
        <td><input type="number" class="arrival-time" /></td>
        <td><input type="number" class="burst-time" /></td>
        <td><input type="number" class="priority" /></td>
        <td><input type="number" class="time-quantum" /></td>
        <td><button class="remove-process">Remove</button></td>
        `;
        processTableBody.appendChild(newRow);
        // Add event listener to the remove button
        newRow.querySelector(".remove-process").addEventListener("click", function () {
            processTableBody.removeChild(newRow);
        });
    });
    // Remove button initial on the first row
    const initialRemoveButton = document.querySelector(".remove-process");
    initialRemoveButton.addEventListener("click", function() {
        processTableBody.removeChild(initialRemoveButton.parentElement.parentElement);
    }); // Calculate button functionality
    calculateButton.addEventListener("click", function () {
        const processes = [];
        const rows = processTableBody.querySelectorAll("tr");
        rows.forEach(row => {
            const processId = row.querySelector(".process-id").value.trim();
            const arrivalTime = parseInt(row.querySelector(".arrival-time").value) || 0;
            const burstTime = parseInt(row.querySelector(".burst-time").value) || 0;
            const priority = parseInt(row.querySelector(".priority").value) || 0;
            const timeQuantum = parseInt(row.querySelector(".time-quantum").value) || 0;
            if (processId) {
                processes.push({ processId, arrivalTime, burstTime, priority, timeQuantum });
            }
        });
        // Call the scheduling algorithm function here
        const results = calculateScheduling(processes);
        displayResults(results);
    });
    function calculateScheduling(processes) {
        // Placeholder for scheduling algorithm calculations
        // You can implement FCFS, SJF, Priority, RR, etc. here
        // For now, we will return dummy data
        return {
            avgWaitingTime: 10,
            avgTurnaroundTime: 15,
            cpuUtilization: 80,
            ganttChart: "Gantt Chart Placeholder"
        };
    }
    function displayResults(results) {
        resultsDiv.innerHTML = `
            <h3>Results</h3>
            <p>Average Waiting Time: \${results.avgWaitingTime}</p>
            <p>Average Turnaround Time: \${results.avgTurnaroundTime}</p>
            <p>CPU Utilization: \${results.cpuUtilization}%</p>
            <p>Gantt Chart: \${results.ganttChart}</p>
        `;
    }
});