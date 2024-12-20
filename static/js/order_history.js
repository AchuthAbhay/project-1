function filterHistory() {
    const query = document.getElementById("search-history").value.toLowerCase();
    const rows = document.querySelectorAll("#status-history-body tr");

    rows.forEach(row => {
        const items = row.children[1].textContent.toLowerCase();
        const address = row.children[5].textContent.toLowerCase();
        row.style.display = (items.includes(query) || address.includes(query)) ? "" : "none";
    });
}
const script = document.currentScript; // Gets the currently executing script
const urlParams = new URLSearchParams(script.src.split('?')[1]);
const customer_id = urlParams.get('customer_id');

if ("serviceWorker" in navigator && "Notification" in window) {
    navigator.serviceWorker
      .register("/service_worker", {
        scope: "/",
      })
      .then(function (registration) {
        console.log(
          "Service Worker registered with scope:",
          registration.scope
        );

        // Request notification permission and automatically subscribe the customer
        Notification.requestPermission().then(function (permission) {
          if (permission === "granted") {
            console.log("Notification permission granted");

            // Automatically subscribe the customer when they visit the page
            const VAPID_PUBLIC_KEY =
              "BBwavOWWblq9rX6faqeNAdEXRWfaRD0rYLgJMCMGcY0SSFHQYDhG7D69cAjHm3RLL3hSxPvsPdBZAqQoMmbEYj8";
            console.log(VAPID_PUBLIC_KEY);
            console.log("Checking service worker readiness...");
            navigator.serviceWorker.ready
              .then(function (registration) {
                console.log("Service worker is ready:", registration);
                // Proceed with subscription logic
              })
              .catch(function (error) {
                console.error("Service worker readiness failed:", error);
              });
            navigator.serviceWorker.ready
              .then(function (registration) {
                return registration.pushManager.subscribe({
                  userVisibleOnly: true,
                  applicationServerKey:
                    urlBase64ToUint8Array(VAPID_PUBLIC_KEY),
                });
              })
              .then(function (subscription) {
                console.log("Customer subscribed:", subscription);



                // Send subscription to the server
                fetch("/subscribe", {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json",
                  },
                  body: JSON.stringify({
                    customer_id: customer_id,
                    subscription: subscription.toJSON(),
                  }),
                }).then((response) => {
                  if (response.ok) {
                    console.log("Subscription saved on server");
                  } else {
                    console.error("Failed to save subscription on server");
                  }
                });
              })
              .catch(function (error) {
                console.error(
                  "Error subscribing to push notifications:",
                  error
                );
              });
          } else {
            console.log("Notification permission denied");
          }
        });
      })
      .catch(function (error) {
        console.log("Service Worker registration failed:", error);
      });
  }

  function urlBase64ToUint8Array(base64String) {
    const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
    const base64 = (base64String + padding)
      .replace(/-/g, "+")
      .replace(/_/g, "/");
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }

