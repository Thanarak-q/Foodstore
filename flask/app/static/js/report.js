$(document).ready(function () {
    fetchAndDrawRevenueChart();

    $("#yearSelector").on("change", function () {
      fetchAndDrawRevenueChart();
    });

    $("#updateChart").click(function () {
      fetchAndDrawRevenueChart();
    });
  });

  let revenueChart;

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