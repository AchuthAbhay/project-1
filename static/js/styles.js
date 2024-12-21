console.log("Hello world!");

document.addEventListener('DOMContentLoaded', function () {
    if (typeof flashed_messages !== 'undefined' && flashed_messages.length > 0) {
        flashed_messages.forEach(message => {
            const [category, text] = message; // Extract category and message text
            toastr.options = {
                "closeButton": true,
                "progressBar": true,
                "positionClass": "toast-top-right custom-toast-top", // Added custom class
                "timeOut": "5000",
            };
            toastr[category](text); // Show the notification
        });
    }
});