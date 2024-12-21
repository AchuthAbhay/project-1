function updateQuantity(itemId, change) {
    const quantityInput = document.getElementById(`quantity-${itemId}`);
    const priceDisplay = document.getElementById(`price-${itemId}`);
    const pricePerItem = parseFloat(priceDisplay.dataset.pricePerItem);
    let currentQuantity = parseInt(quantityInput.value);

    // Update Quantity
    const newQuantity = Math.max(1, Math.min(10, currentQuantity + change)); // Ensure quantity is between 1 and 10

    // Make the POST request to update the server
    fetch(`/update_cart/${itemId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': '{{ csrf_token() }}'
        },
        body: `quantity=${newQuantity}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the quantity input
            quantityInput.value = newQuantity;

            // Update the price for this cart item
            priceDisplay.textContent = `₹${(newQuantity * pricePerItem).toFixed(2)}`;

            // Update the order summary
            updateOrderSummary();
        } else {
            alert(`Error: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to update cart. Please try again.');
    });
}

function updateOrderSummary() {
    fetch('/cart_summary', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the Order Summary fields
            document.querySelector('.order-summary-details p:nth-child(1) span').textContent = `₹${data.subtotal.toFixed(2)}`;
            document.querySelector('.order-summary-details p:nth-child(2) span').textContent = `₹${data.shipping_cost.toFixed(2)}`;
            document.querySelector('.order-summary-details p:nth-child(3) span').textContent = `${data.total_weight.toFixed(2)} kg`;
            document.querySelector('.order-summary-total span').textContent = `₹${data.total_price_with_shipping.toFixed(2)}`;
        } else {
            alert(`Error: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to update order summary. Please try again.');
    });
}


