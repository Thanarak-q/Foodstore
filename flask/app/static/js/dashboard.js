$(document).ready(function () {
  // ตั้งค่า default เป็นวันนี้
  const today = new Date();
  const startDate = new Date(today);
  startDate.setHours(0, 0, 0, 0);
  const endDate = new Date(today);
  endDate.setHours(23, 59, 59, 999);

  $("#startDate").val(startDate.toISOString().split("T")[0]);
  $("#endDate").val(endDate.toISOString().split("T")[0]);

  // เรียกฟังก์ชันเพื่อดึงข้อมูลเริ่มต้น
  fetchTotalSale();
  fetchTotalOrder();
  fetchtotalMenuItems();
  fetchTop5Menus();
  fetchAndDrawRevenueChart();
  fetchLatestReviews(); 

  // แก้ไข: เพิ่มการสลับแสดง Filter Container
  $("#toggleFilterButton").click(function () {
    $("#filterContainer").toggleClass("is-hidden");
  });

  // ฟังก์ชันที่มีอยู่แล้ว
  $("#filterButton").click(function () {
    fetchTotalSale();
    fetchTotalOrder();
    fetchTop5Menus(); // เพิ่มการอัปเดต Top 5 Menus เมื่อกดปุ่ม Filter
  });

  $("#resetButton").click(function () {
    $("#startDate").val("");
    $("#endDate").val("");
    fetchTotalSale();
    fetchTotalOrder();
    fetchTop5Menus(); // เพิ่มการอัปเดต Top 5 Menus เมื่อกดปุ่ม Reset
  });

  $("#timeRange").change(function () {
    const selectedRange = $(this).val();
    const today = new Date();
    let startDate, endDate;

    // ซ่อน/แสดง input วันที่
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
        // เมื่อเลือก custom จะให้แสดงวันที่ที่เลือก
        const customStartDate = $("#startDate").val();
        const customEndDate = $("#endDate").val();
        startDate = new Date(customStartDate);
        endDate = new Date(customEndDate);
        break;
      default:
        startDate = null;
        endDate = null;
        break;
    }

    if (startDate && endDate) {
      $("#startDate").val(startDate.toISOString().split("T")[0]);
      $("#endDate").val(endDate.toISOString().split("T")[0]);
      // แสดงช่วงเวลาที่เลือกในปุ่ม Filter
      $("#filterPeriodLabel").text(`${selectedRange.charAt(0).toUpperCase() + selectedRange.slice(1)}`);
    } else {
      $("#startDate").val("");
      $("#endDate").val("");
      $("#filterPeriodLabel").text("Select Range");
    }

    // เรียกฟังก์ชันเพื่ออัปเดตข้อมูล
    fetchTotalSale();
    fetchTotalOrder();
    fetchTop5Menus(); // เพิ่มการอัปเดต Top 5 Menus เมื่อเปลี่ยนช่วงเวลา
  });
});

function fetchTotalSale() {
  const selectedRange = $("#timeRange").val(); // ตรวจสอบช่วงเวลาที่เลือก
  const startDate = $("#startDate").val();
  const endDate = $("#endDate").val();

  $.getJSON("/payment/get_all_payment", function (data) {
    let filteredData = data;

    // กรองข้อมูลตามวันที่เฉพาะเมื่อไม่ใช่โหมด "All Time"
    if (selectedRange !== "all_time" && startDate && endDate) {
      filteredData = data.filter((payment) => {
        const paymentTime = new Date(payment.payment_time);
        const start = new Date(startDate);
        const end = new Date(endDate);
        return paymentTime >= start && paymentTime <= end;
      });
    }

    // คำนวณยอดขายรวม
    const totalSale = filteredData.reduce(
      (acc, pay) => acc + (Number(pay.amount) || 0),
      0
    );

    // แสดงผลยอดขายรวม
    $("#totalSale").text(`฿ ${totalSale.toLocaleString()}`);
  }).fail(function (jqXHR, textStatus, errorThrown) {
    console.error("Error fetching payment data:", textStatus, errorThrown);
    $("#totalSale").text("เกิดข้อผิดพลาดในการดึงข้อมูล");
  });
}

function fetchTotalOrder() {
  const selectedRange = $("#timeRange").val();
  const startDate = $("#startDate").val();
  const endDate = $("#endDate").val();

  $.getJSON("/orders/get_all_orders", function (data) {
    let filteredData = data;

    // กรองข้อมูลตามวันที่เฉพาะเมื่อไม่ใช่โหมด "All Time"
    if (selectedRange !== "all_time" && startDate && endDate) {
      filteredData = data.filter((order) => {
        const orderTime = new Date(order.order_time);
        const start = new Date(startDate);
        const end = new Date(endDate);
        return orderTime >= start && orderTime <= end;
      });
    }

    const totalOrder = filteredData.length;
    $("#totalOrder").text(`${totalOrder.toLocaleString()}`);
    
    // คำนวณ Average Order Value
    if (totalOrder > 0) {
      $.getJSON("/payment/get_all_payment", function (paymentData) {
        let filteredPaymentData = paymentData;
        
        // กรองข้อมูลการชำระเงินตามวันที่
        if (selectedRange !== "all_time" && startDate && endDate) {
          filteredPaymentData = paymentData.filter((payment) => {
            const paymentTime = new Date(payment.payment_time);
            const start = new Date(startDate);
            const end = new Date(endDate);
            return paymentTime >= start && paymentTime <= end;
          });
        }
        
        const totalSale = filteredPaymentData.reduce(
          (acc, pay) => acc + (Number(pay.amount) || 0),
          0
        );
        
        const avgOrderValue = totalSale / totalOrder;
        $("#avgOrderValue").text(`฿ ${avgOrderValue.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`);
      });
    } else {
      $("#avgOrderValue").text("฿ 0.00");
    }
  });
}

function fetchtotalMenuItems() {
  $.getJSON("/menus/get_all_menus", function (menuData) {
    const totalMenuItems = menuData.length;
    $("#totalMenuItems").text(totalMenuItems);
  });
}

function fetchTop5Menus() {
  const selectedRange = $("#timeRange").val();
  const startDate = $("#startDate").val();
  const endDate = $("#endDate").val();
  let apiUrl;

  // กำหนด API URL ตามช่วงเวลาที่เลือก
  switch (selectedRange) {
    case "day":
      apiUrl = "/daily_trending";
      break;
    case "week":
      apiUrl = "/weekly_trending";
      break;
    case "month":
      apiUrl = "/monthly_trending";
      break;
    case "year":
      apiUrl = "/yearly_trending";
      break;
    case "custom":
      // ใช้ custom API endpoint พร้อมส่งพารามิเตอร์วันที่
      if (startDate && endDate) {
        apiUrl = `/custom_trending?start_date=${startDate}&end_date=${endDate}`;
        console.log(apiUrl);
      } else {
        apiUrl = "/all_time_trending";
      }
      break;
    case "all_time":
      apiUrl = "/all_time_trending";
      break;
    default:
      apiUrl = "/all_time_trending";
      break;
  }

  // แสดง loading indicator
  $("#top5OrderMenus").html('<div class="has-text-centered"><p>กำลังโหลดข้อมูล...</p></div>');

  // ดึงข้อมูลจาก API
  $.getJSON(apiUrl, function (data) {
    const top5OrderMenus = data.slice(0, 5); // เลือกเฉพาะ 5 อันดับแรก
    let htmlContent = '';

    if (top5OrderMenus.length === 0) {
      htmlContent = '<div class="has-text-centered"><p>ไม่พบข้อมูลเมนูในช่วงเวลาที่เลือก</p></div>';
    } else {
      // สร้าง HTML สำหรับแสดงผลเมนู
      top5OrderMenus.forEach((menu, index) => {
        htmlContent += `
          <div class="media">
            <div class="media-left">
              <figure class="image is-128x128">
                <!-- Apply CSS styles for cropping and centering -->
                <img src="${menu.image_url}" alt="${menu.menu_name}" style="width: 100%; height: 100%; object-fit: cover; object-position: center;">
              </figure>
            </div>
            <div class="media-content">
              <p class="title is-4 has-text-weight-bold">${index + 1}. ${menu.menu_name}</p>
              <p class="subtitle is-6 has-text-grey-dark">จำนวนการสั่ง: <strong>${menu.total_sold} ครั้ง</strong></p>
            </div>
          </div>
        `;
      });
    }

    // แสดงผลใน #top5OrderMenus
    $("#top5OrderMenus").html(htmlContent);
  }).fail(function (jqXHR, textStatus, errorThrown) {
    console.error("Error fetching trending menus:", textStatus, errorThrown);
    $("#top5OrderMenus").html("<p>เกิดข้อผิดพลาดในการดึงข้อมูลเมนูเทรนด์</p>");
  });
}

function checkMenuPerformance(menuData) {
  const averageSales =
    menuData.reduce((sum, menu) => sum + menu.ordered, 0) / menuData.length;

  menuData.forEach((menu) => {
    if (menu.ordered > averageSales * 1.5) {
      showNotification(`${menu.name} is selling fast!`, "is-success");
    } else if (menu.ordered < averageSales * 0.5) {
      showNotification(`${menu.name} is underperforming`, "is-warning");
    }
  });
}

function showNotification(message, type) {
  const notification = $(
    `<div class="notification ${type}">
      <button class="delete"></button>
      ${message}
    </div>`
  );

  $("#notifications").append(notification);

  notification.find(".delete").click(function () {
    notification.remove();
  });

  setTimeout(() => notification.remove(), 5000);
}

let revenueChart;

function populateYearSelector(data) {
  const years = [
    ...new Set(
      data.map((payment) => new Date(payment.payment_time).getFullYear())
    ),
  ]
    .sort()
    .reverse();

  const $yearSelector = $("#yearSelector");
  const currentYear = new Date().getFullYear();

  years.forEach((year) => {
    const isSelected = year === currentYear ? "selected" : "";
    $yearSelector.append(
      `<option value="${year}" ${isSelected}>${year}</option>`
    );
  });

  $yearSelector.select2({
    placeholder: "Select years to compare",
    allowClear: true,
    width: "100%",
  });

  // Trigger change เพื่อให้กราฟแสดงผลทันทีหลังจาก populate
  $yearSelector.trigger("change");
}

function fetchAndDrawRevenueChart() {
  const selectedYears = $("#yearSelector").val() || [];

  $.getJSON("/payment/get_all_payment", function (data) {
    // Populate year selector on first load
    if ($("#yearSelector").children().length === 1) {
      populateYearSelector(data);
    }

    // Prepare monthly revenue data
    const monthlyRevenue = {};
    data.forEach((payment) => {
      const date = new Date(payment.payment_time);
      const year = date.getFullYear();
      const month = date.getMonth();
      const amount = Number(payment.amount) || 0;

      if (!monthlyRevenue[year]) {
        monthlyRevenue[year] = Array(12).fill(0);
      }
      monthlyRevenue[year][month] += amount;
    });

    const ctx = document.getElementById("revenueChart").getContext("2d");
    if (revenueChart) {
      revenueChart.destroy();
    }

    const colors = [
      "rgb(75, 192, 192)",
      "rgb(255, 99, 132)",
      "rgb(54, 162, 235)",
      "rgb(255, 206, 86)",
      "rgb(153, 102, 255)",
      "rgb(255, 159, 64)",
      "rgb(199, 199, 199)",
      "rgb(83, 83, 83)",
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
        labels: [
          "Jan",
          "Feb",
          "Mar",
          "Apr",
          "May",
          "Jun",
          "Jul",
          "Aug",
          "Sep",
          "Oct",
          "Nov",
          "Dec",
        ],
        datasets: datasets,
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: "Revenue (฿)",
            },
            ticks: {
              callback: function (value) {
                return "฿" + value.toLocaleString();
              },
            },
          },
          x: {
            title: {
              display: true,
              text: "Month",
            },
          },
        },
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: "Monthly Revenue Comparison",
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                let label = context.dataset.label || "";
                if (label) {
                  label += ": ";
                }
                label += "฿" + context.parsed.y.toLocaleString();
                return label;
              },
            },
          },
        },
      },
    });
  }).fail(function (jqXHR, textStatus, errorThrown) {
    console.error("Error fetching data:", textStatus, errorThrown);
  });
}
function fetchLatestReviews() {
  $.getJSON("/reviews/get_all_reviews", function (reviewData) {
    console.log(reviewData)
    const reviewContainer = $("#ReviewRes");
    reviewContainer.empty();
    let htmlContent = '';
    let count = 0;
    let reviews = reviewData.reviews.slice().reverse();
    for (i of reviews){
      if(count >= 5) break;
      count++;
          htmlContent += 
            `<div class="media">
               <div class="media-content">
                 <p class="subtitle is-6">โดย: ${i.name}</p>
              <p class="subtitle is-6">คะแนน: ${i.star}</p>
              <p class="subtitle is-6">รีวิว: ${i.review}</p>
               </div>
             </div>
             <hr>`;
    }
    reviewContainer.html(htmlContent);
  });
}

$(document).ready(function () {
  // เรียกฟังก์ชันเริ่มต้นเมื่อโหลดหน้า
  fetchLatestReviews();
  fetchTop5Menus();

  // เมื่อผู้ใช้เลือกช่วงเวลา
  $("#timeRange").change(function () {
    if ($(this).val() === "custom") {
      $("#startDateContainer").show();
      $("#endDateContainer").show();
    } else {
      $("#startDateContainer").hide();
      $("#endDateContainer").hide();
    }
    fetchTop5Menus();
  });

  // เมื่อผู้ใช้กดปุ่ม Filter
  $("#filterButton").click(function () {
    fetchTop5Menus();
  });
  
});
