$(document).ready(function () {
  // ตั้งค่าเริ่มต้นเป็นวันนี้
  const today = new Date();
  const startDate = new Date(today.setHours(0, 0, 0, 0));
  const endDate = new Date(today.setHours(23, 59, 59, 999));
  $("#startDate").val(startDate.toISOString().split("T")[0]);
  $("#endDate").val(endDate.toISOString().split("T")[0]);

  // เรียกฟังก์ชันเริ่มต้น
  fetchTotalSale();
  fetchTotalOrder();
  fetchtotalMenuItems();
  fetchTop5Menus();
  fetchLatestReviews();

  // Toggle Filter Container
  $("#toggleFilterButton").click(function () {
    $("#filterContainer").toggleClass("is-hidden");
  });

  // Filter Button
  $("#filterButton").click(function () {
    fetchTotalSale();
    fetchTotalOrder();
    fetchTop5Menus();
  });

  // Time Range Change
  $("#timeRange").change(function () {
    const selectedRange = $(this).val();
    const today = new Date();
    let startDate, endDate;

    $("#startDateContainer, #endDateContainer").toggle(selectedRange === "custom");

    switch (selectedRange) {
      case "day":
        startDate = new Date(today.setHours(0, 0, 0, 0));
        endDate = new Date(today.setHours(23, 59, 59, 999));
        break;
      case "week":
        startDate = new Date(today);
        startDate.setDate(today.getDate() - today.getDay());
        endDate = new Date(startDate);
        endDate.setDate(startDate.getDate() + 6);
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
        const customStart = $("#startDate").val();
        const customEnd = $("#endDate").val();
        if (customStart && customEnd) {
          startDate = new Date(customStart);
          endDate = new Date(customEnd);
          endDate.setHours(23, 59, 59, 999);
        }
        break;
    }

    if (startDate && endDate) {
      $("#startDate").val(startDate.toISOString().split("T")[0]);
      $("#endDate").val(endDate.toISOString().split("T")[0]);
      $("#filterPeriodLabel").text(
        selectedRange === "custom" ? "Custom" : selectedRange.charAt(0).toUpperCase() + selectedRange.slice(1)
      );
    } else if (selectedRange === "all_time") {
      $("#startDate, #endDate").val("");
      $("#filterPeriodLabel").text("All Time");
    }

    fetchTotalSale();
    fetchTotalOrder();
    fetchTop5Menus();
  });
});

// Fetch Functions
function fetchTotalSale() {
  const startDateStr = $("#startDate").val();
  const endDateStr = $("#endDate").val();
  const selectedRange = $("#timeRange").val();

  $("#totalSale").text("กำลังโหลด...");

  $.getJSON("/payment/get_all_payment", function (data) {
    let filteredData = data;
    if (selectedRange !== "all_time" && startDateStr && endDateStr) {
      const start = new Date(startDateStr);
      const end = new Date(endDateStr).setHours(23, 59, 59, 999);
      filteredData = data.filter(payment => {
        const paymentTime = new Date(payment.payment_time);
        return paymentTime >= start && paymentTime <= end;
      });
    }

    const totalSale = filteredData.reduce((acc, pay) => acc + (Number(pay.amount) || 0), 0);
    $("#totalSale").text(`฿ ${totalSale.toLocaleString()}`);
  }).fail(function () {
    $("#totalSale").text("เกิดข้อผิดพลาด");
  });
}

function fetchTotalOrder() {
  const startDateStr = $("#startDate").val();
  const endDateStr = $("#endDate").val();
  const selectedRange = $("#timeRange").val();

  $.getJSON("/orders/get_all_orders", function (data) {
    let filteredData = data;
    if (selectedRange !== "all_time" && startDateStr && endDateStr) {
      const start = new Date(startDateStr);
      const end = new Date(endDateStr).setHours(23, 59, 59, 999);
      filteredData = data.filter(order => {
        const orderTime = new Date(order.order_time);
        return orderTime >= start && orderTime <= end;
      });
    }

    $("#totalOrder").text(filteredData.length.toLocaleString());
  }).fail(function () {
    $("#totalOrder").text("เกิดข้อผิดพลาด");
  });
}

function fetchtotalMenuItems() {
  $.getJSON("/menus/get_all_menus", function (data) {
    $("#totalMenuItems").text(data.length);
  }).fail(function () {
    $("#totalMenuItems").text("เกิดข้อผิดพลาด");
  });
}

function fetchTop5Menus() {
  const selectedRange = $("#timeRange").val();
  const startDate = $("#startDate").val();
  const endDate = $("#endDate").val();
  
  let apiUrl = {
    "day": "/daily_trending",
    "week": "/weekly_trending",
    "month": "/monthly_trending",
    "year": "/yearly_trending",
    "all_time": "/all_time_trending",
    "custom": startDate && endDate ? 
      `/custom_trending?start_date=${startDate}&end_date=${endDate}` : 
      "/all_time_trending"
  }[selectedRange] || "/all_time_trending";

  $("#top5OrderMenus").html('<div class="has-text-centered"><p>กำลังโหลดข้อมูล...</p></div>');

  $.getJSON(apiUrl, function (data) {
    const top5 = data.slice(0, 5);
    let htmlContent = top5.length ? 
      top5.map((menu, index) => `
        <div class="media">
          <div class="media-left">
            <figure class="image is-128x128" style="width: 4rem; height: 4rem; overflow: hidden;">
              <img src="${menu.image_url}" alt="${menu.menu_name}" 
                style="width: 100%; height: 100%; object-fit: cover; object-position: center;">
            </figure>
          </div>
          <div class="media-content">
            <p class="title is-4 has-text-weight-bold">${index + 1}. ${menu.menu_name}</p>
            <p class="subtitle is-6 has-text-grey-dark">จำนวนการสั่ง: <strong>${menu.total_sold} ครั้ง</strong></p>
          </div>
        </div>
      `).join('') :
      '<div class="has-text-centered"><p>ไม่พบข้อมูลเมนูในช่วงเวลาที่เลือก</p></div>';

    $("#top5OrderMenus").html(htmlContent);
  }).fail(function () {
    $("#top5OrderMenus").html("<p>เกิดข้อผิดพลาดในการดึงข้อมูล</p>");
  });
}

function fetchLatestReviews() {
  $.getJSON("/reviews/get_all_reviews", function (data) {
    const reviews = data.reviews.slice().reverse().slice(0, 5);
    const htmlContent = reviews.map(review => `
      <div class="media">
        <div class="media-content">
          <p class="subtitle is-6">โดย: ${review.name} คะแนน: ${generateStars(review.star)}</p>
          <p class="subtitle is-6">รีวิว: ${review.review}</p>
        </div>
      </div>
      <hr>
    `).join('');
    
    $("#ReviewRes").html(htmlContent);
  }).fail(function () {
    $("#ReviewRes").html("<p>เกิดข้อผิดพลาดในการดึงข้อมูล</p>");
  });
}

function generateStars(rating) {
  return '⭐'.repeat(rating) + '☆'.repeat(5 - rating);
}