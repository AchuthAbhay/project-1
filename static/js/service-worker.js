// Listener for push events
self.addEventListener('push', function(event) {
  // Parse the payload if it is JSON
  let payload = {};
  try {
      payload = event.data ? JSON.parse(event.data.text()) : {};
  } catch (e) {
      console.error('Failed to parse push event payload:', e);
  }
  const title = payload.title || 'Delivery Status Update'; // Default title
  const body = payload.body || 'Your delivery status has been updated.';
//   const icon = payload.icon || '/static/icon.png'; // Default icon path
//   const badge = payload.badge || '/static/badge.png'; // Default badge path
  const url = payload.url || '/customer-dashboard'; // Fallback to dashboard

  const options = {
      body: body,
    //   icon: icon,
    //   badge: badge,
      data: { url: url } // Include the URL to open
  };

  event.waitUntil(
      self.registration.showNotification(title, options)
  );
});

// Listener for notification click events
self.addEventListener('notificationclick', function(event) {
  event.notification.close(); // Close the notification

  const urlToOpen = event.notification.data.url;

  event.waitUntil(
      clients.matchAll({ type: 'window', includeUncontrolled: true }).then(windowClients => {
          // Check if the relevant page is already open
          for (let client of windowClients) {
              if (client.url === urlToOpen && 'focus' in client) {
                  return client.focus();
              }
          }
          // Open the URL in a new window if no match
          if (clients.openWindow) {
              return clients.openWindow(urlToOpen);
          }
      })
  );
});
