$(document).ready(function () {
    const today = new Date();
    const startDate = new Date(today);
    startDate.setHours(0, 0, 0, 0);
    const endDate = new Date(today);
    endDate.setHours(23, 59, 59, 999);

    $("#startDate").val(startDate.toISOString().split("T")[0]);
    $("#endDate").val(endDate.toISOString().split("T")[0]);

    fetchTotalSale();
    fetchTotalOrder();
    fetchtotalMenuItems();

    $("#toggleFilterButton").click(function () {
      $("#filterContainer").toggleClass("is-hidden");
    });

    $("#filterButton").click(function () {
      fetchTotalSale();
      fetchTotalOrder();
    });

    $("#timeRange").change(function () {
      const selectedRange = $(this).val();
      const today = new Date();
      let startDate, endDate;

      if (selectedRange === "custom") {
        $("#startDateContainer").show();
        $("#endDateContainer").show();
      } else {
        $("#startDateContainer").hide();
        $("#endDateContainer").hide();
      }

      switch (selectedRange) {
        case "day":
          startDate = new Date(today);
          startDate.setHours(0, 0, 0, 0);
          endDate = new Date(today);
          endDate.setHours(23, 59, 59, 999);
          break;
        case "week":
          startDate = new Date(today);
          startDate.setDate(today.getDate() - today.getDay());
          startDate.setHours(0, 0, 0, 0);
          endDate = new Date(today);
          endDate.setDate(today.getDate() + (6 - today.getDay()));
          endDate.setHours(23, 59, 59, 999);
          break;
        case "month":
          startDate = new Date(today.getFullYear(), today.getMonth(), 1);
          endDate = new Date(today.getFullYear(), today.getMonth() + 1, 0);
          endDate.setHours(23, 59, 59, 999);
          break;
        case "year":
          startDate = new Date(today.getFullYear(), 0, 1);
          endDate = new Date(today.getFullYear(), 11, 31);
          endDate.setHours(23, 59, 59, 999);
          break;
        case "custom":
          const customStartDate = $("#startDate").val();
          const customEndDate = $("#endDate").val();
          startDate = new Date(customStartDate);
          endDate = new Date(customEndDate);
          break;
      }

      if (startDate && endDate) {
        $("#startDate").val(startDate.toISOString().split("T")[0]);
        $("#endDate").val(endDate.toISOString().split("T")[0]);
        $("#filterPeriodLabel").text(`${selectedRange.charAt(0).toUpperCase() + selectedRange.slice(1)}`);
      } else {
        $("#startDate").val("");
        $("#endDate").val("");
        $("#filterPeriodLabel").text("Select Range");
      }

      fetchTotalSale();
      fetchTotalOrder();
    });
  });

  function fetchTotalSale() {
    $.getJSON("/payment/get_all_payment", function (data) {
      const totalSale = data.reduce((acc, pay) => acc + (Number(pay.amount) || 0), 0);
      $("#totalSale").text(`฿ ${totalSale.toLocaleString()}`);
    });
  }

  function fetchTotalOrder() {
    $.getJSON("/orders/get_all_orders", function (data) {
      $("#totalOrder").text(`${data.length.toLocaleString()}`);
    });
  }

  function fetchtotalMenuItems() {
    $.getJSON("/menus/get_all_menus", function (menuData) {
      $("#totalMenuItems").text(menuData.length);
    });
  }