$(document).ready(function () {
  fetchAndDrawRevenueChart();
  fetchAndDrawCustomerChart(); // Initialize customer chart
  fetchAndDrawPaymentMethodChart(); // Initialize payment methods chart
  fetchAndDrawEmployeeRolesChart(); // Initialize employee roles chart

  $("#yearSelector").on("change", function () {
    fetchAndDrawRevenueChart();
  });

  $("#updateChart").click(function () {
    fetchAndDrawRevenueChart();
  });

  $("#customerTimeSelector").on("change", function () {
    fetchAndDrawCustomerChart(); // Update customer chart when selector changes
  });

  $("#paymentMethodTimeSelector").on("change", function () {
    fetchAndDrawPaymentMethodChart(); // Update payment methods chart when selector changes
  });
});

let revenueChart;
let customerChart;
let paymentMethodChart;
let employeeRolesChart;

function populateYearSelector(data) {
  const years = [...new Set(data.map((p) => new Date(p.payment_time).getFullYear()))].sort().reverse();
  const $yearSelector = $("#yearSelector");
  const currentYear = new Date().getFullYear();

  years.forEach((year) => {
    const isSelected = year === currentYear ? "selected" : "";
    $yearSelector.append(`<option value="${year}" ${isSelected}>${year}</option>`);
  });

  $yearSelector.select2({
    placeholder: "Select years to compare",
    allowClear: true,
    width: "100%",
  });

  $yearSelector.trigger("change");
}

function fetchAndDrawRevenueChart() {
  const selectedYears = $("#yearSelector").val() || [];

  $.getJSON("/payment/get_all_payment", function (data) {
    if ($("#yearSelector").children().length === 1) populateYearSelector(data);

    const monthlyRevenue = {};
    data.forEach((p) => {
      const date = new Date(p.payment_time);
      const year = date.getFullYear();
      const month = date.getMonth();
      const amount = Number(p.amount) || 0;
      if (!monthlyRevenue[year]) monthlyRevenue[year] = Array(12).fill(0);
      monthlyRevenue[year][month] += amount;
    });

    const ctx = document.getElementById("revenueChart").getContext("2d");
    if (revenueChart) revenueChart.destroy();

    const colors = [
      "rgb(75, 192, 192)",
      "rgb(255, 99, 132)",
      "rgb(54, 162, 235)",
      "rgb(255, 206, 86)",
      "rgb(153, 102, 255)",
      "rgb(255, 159, 64)",
    ];

    const datasets = selectedYears.map((year, index) => ({
      label: `Revenue ${year}`,
      data: monthlyRevenue[year] || Array(12).fill(0),
      borderColor: colors[index % colors.length],
      tension: 0.1,
    }));

    revenueChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: datasets,
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            title: { display: true, text: "Revenue (฿)" },
            ticks: { callback: (v) => "฿" + v.toLocaleString() },
          },
          x: { title: { display: true, text: "Month" } },
        },
        plugins: {
          legend: { position: "top" },
          title: { display: true, text: "Monthly Revenue Comparison" },
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.dataset.label}: ฿${ctx.parsed.y.toLocaleString()}`,
            },
          },
        },
      },
    });
  }).fail((jqXHR, textStatus, errorThrown) => {
    console.error("Error fetching data:", textStatus, errorThrown);
  });
}

// Function to fetch and draw customer chart
function fetchAndDrawCustomerChart() {
  const timeFrame = $("#customerTimeSelector").val();
  const apiUrl = `/${timeFrame}_customers`;

  $.getJSON(apiUrl, function (data) {
    const daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    const customerData = daysOfWeek.map((day) => data[day] || 0);

    const ctx = document.getElementById("customerChart").getContext("2d");
    if (customerChart) customerChart.destroy();

    customerChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: daysOfWeek,
        datasets: [
          {
            label: `Number of Customers (${timeFrame.replace("_", " ")})`,
            data: customerData,
            backgroundColor: "rgba(54, 162, 235, 0.5)",
            borderColor: "rgb(54, 162, 235)",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            title: { display: true, text: "Number of Customers" },
          },
          x: { title: { display: true, text: "Day of the Week" } },
        },
        plugins: {
          legend: { position: "top" },
          title: { display: true, text: `Customer Insights (${timeFrame.replace("_", " ")})` },
        },
      },
    });
  }).fail((jqXHR, textStatus, errorThrown) => {
    console.error("Error fetching customer data:", textStatus, errorThrown);
  });
}

// Function to fetch and draw payment methods chart
function fetchAndDrawPaymentMethodChart() {
  const timeFrame = $("#paymentMethodTimeSelector").val();
  const apiUrl = `/${timeFrame}_payment_methods`;

  $.getJSON(apiUrl, function (data) {
    const paymentMethods = Object.keys(data);
    const paymentData = Object.values(data);

    const ctx = document.getElementById("paymentMethodChart").getContext("2d");
    if (paymentMethodChart) paymentMethodChart.destroy();

    paymentMethodChart = new Chart(ctx, {
      type: "pie",
      data: {
        labels: paymentMethods,
        datasets: [
          {
            label: `Payment Methods (${timeFrame.replace("_", " ")})`,
            data: paymentData,
            backgroundColor: [
              "rgba(255, 99, 132, 0.5)",
              "rgba(54, 162, 235, 0.5)",
              "rgba(75, 192, 192, 0.5)",
              "rgba(255, 206, 86, 0.5)",
              "rgba(153, 102, 255, 0.5)",
              "rgba(255, 159, 64, 0.5)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "top" },
          title: { display: true, text: `Payment Methods (${timeFrame.replace("_", " ")})` },
        },
      },
    });
  }).fail((jqXHR, textStatus, errorThrown) => {
    console.error("Error fetching payment methods data:", textStatus, errorThrown);
  });
}

// Function to fetch and draw employee roles chart
function fetchAndDrawEmployeeRolesChart() {
  const apiUrl = "/employee_roles_distribution";

  $.getJSON(apiUrl, function (data) {
    const roles = Object.keys(data);
    const roleCounts = Object.values(data);

    const ctx = document.getElementById("employeeRolesChart").getContext("2d");
    if (employeeRolesChart) employeeRolesChart.destroy();

    employeeRolesChart = new Chart(ctx, {
      type: "pie",
      data: {
        labels: roles,
        datasets: [
          {
            label: "Employee Roles Distribution",
            data: roleCounts,
            backgroundColor: [
              "rgba(255, 99, 132, 0.5)",
              "rgba(54, 162, 235, 0.5)",
              "rgba(75, 192, 192, 0.5)",
              "rgba(255, 206, 86, 0.5)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(255, 206, 86, 1)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "top" },
          title: { display: true, text: "Employee Roles Distribution" },
        },
      },
    });
  }).fail((jqXHR, textStatus, errorThrown) => {
    console.error("Error fetching employee roles data:", textStatus, errorThrown);
  });
}