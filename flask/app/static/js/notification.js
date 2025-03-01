function fetchNotifications() {
    $.get("/api/notifications", function (data) {
      let notificationsDiv = $("#notifications");
      let notificationCount = $(".notification-count");
      notificationsDiv.empty();
      notificationCount.text(data.length);
  
      data.forEach(function (notif) {
        let notificationItem = $(`
          <div class="notification-item">
            <div class="notification-card ${notif.type === "order" ? "notif-success" : "notif-warning"}">
              <div class="notif-header">
                <span class="notif-type">${notif.type.toUpperCase()}</span>
                <span class="notif-time">${new Date(notif.created_at).toLocaleTimeString()}</span>
              </div>
              <div class="notif-message">${notif.message}</div>
              <div class="notif-actions">
                <button class="btn btn-view">
                  <a href="${notif.link}">View Details</a>
                </button>
                <button class="btn btn-delete" data-id="${notif.notification_id}">Delete</button>
              </div>
            </div>
          </div>
        `);
        notificationsDiv.append(notificationItem);
      });
    }).fail(function (error) {
      console.error("Error fetching notifications:", error);
    });
  }
  
  $(document).on("click", ".btn-delete", function () {
    let notificationId = $(this).data("id");
    console.log("Deleting notification with ID:", notificationId);
    $.ajax({
      url: `/api/notifications/${notificationId}`,
      type: "DELETE",
      success: function (data) {
        console.log("Notification deleted:", data);
        fetchNotifications();
      },
      error: function (error) {
        console.error("Error deleting notification:", error);
      },
    });
  });
  