// Function to filter orders based on the search input
function filterPendingOrders() {
    const input = document.getElementById('search-pending').value.toLowerCase();
    const tableRows = document.querySelectorAll('#pending-orders-table tbody tr');
    
    tableRows.forEach(row => {
        const customerName = row.querySelector('td').textContent.toLowerCase();
        if (customerName.includes(input)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Function to dynamically allow only certain status changes
function restrictStatusChanges() {
    const tableRows = document.querySelectorAll('#pending-orders-table tbody tr');
    
    tableRows.forEach(row => {
        const currentStatus = row.querySelector('td:nth-child(6)').textContent.trim();
        const statusDropdown = row.querySelector('.status-dropdown');
        
        // Disable options that aren't allowed based on the current status
        Array.from(statusDropdown.options).forEach(option => {
            if (isAllowedStatusChange(currentStatus, option.value)) {
                option.disabled = false;
            } else {
                option.disabled = true;
            }
        });
    });
}

// Function to determine if a status change is allowed
function isAllowedStatusChange(currentStatus, newStatus) {
    const allowedTransitions = {
        'Picked Up': ['In Transit', 'Failed Delivery'],
        'In Transit': ['Delivered', 'Failed Delivery'],
        'Failed Delivery': ['Picked Up'],
        'Delivered': [] // No transitions allowed from 'Delivered'
    };

    return allowedTransitions[currentStatus] && allowedTransitions[currentStatus].includes(newStatus);
}

// Function to handle status change with confirmation and reason handling
function handleStatusChange(selectElement) {
    const newStatus = selectElement.value;
    const form = selectElement.closest('.status-form');
    const currentStatus = form.closest('tr').querySelector('.current-status').textContent.trim();

    if (newStatus === 'Failed Delivery') {
        const reason = prompt("Please provide a reason for 'Failed Delivery':");

        if (!reason) {
            alert('Reason is required for "Failed Delivery".');
            selectElement.value = currentStatus; // Revert to the original status
            return;
        }

        // Add the reason to the form before submitting
        const reasonField = document.createElement('input');
        reasonField.type = 'hidden';
        reasonField.name = 'reason';
        reasonField.value = reason;
        form.appendChild(reasonField);

        if (isAllowedStatusChange(currentStatus, newStatus)) {
            if (confirm(`Are you sure you want to change the status to "${newStatus}"?`)) {
                form.submit();
            } else {
                // Revert to the original status if not confirmed
                selectElement.value = currentStatus;
            }
        } else {
            alert(`Changing status from "${currentStatus}" to "${newStatus}" is not allowed.`);
            selectElement.value = currentStatus; // Revert back to the original status
        }
    } else {
        // If status is not "Failed Delivery", just submit the form
        if (isAllowedStatusChange(currentStatus, newStatus)) {
            if (confirm(`Are you sure you want to change the status to "${newStatus}"?`)) {
                form.submit();
            } else {
                selectElement.value = currentStatus; // Revert back to the original status
            }
        } else {
            alert(`Changing status from "${currentStatus}" to "${newStatus}" is not allowed.`);
            selectElement.value = currentStatus; // Revert back to the original status
        }
    }
}

// Function to refresh orders from the server
function refreshPendingOrders() {
    const courierId = document.getElementById('courier-id').value; // Hidden input for courier ID
    fetch(`/courier/${courierId}/orders?json=true`)
        .then(response => response.json())
        .then(data => {
            const ordersTableBody = document.getElementById('pending-orders-body');
            ordersTableBody.innerHTML = ''; // Clear the current table

            data.orders.forEach(order => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${order.customer_name}</td>
                    <td>${order.customer_address}</td>
                    <td>${order.products}</td>
                    <td>${order.quantity}</td>
                    <td>${order.estimated_delivery}</td>
                    <td>${order.status}</td>
                    <td>
                        <select class="status-dropdown">
                            <option value="picked_up" ${order.status === 'Picked Up' ? 'selected' : ''}>Picked Up</option>
                            <option value="in_transit" ${order.status === 'In Transit' ? 'selected' : ''}>In Transit</option>
                            <option value="delivered" ${order.status === 'Delivered' ? 'selected' : ''}>Delivered</option>
                            <option value="failed_delivery" ${order.status === 'Failed Delivery' ? 'selected' : ''}>Failed Delivery</option>
                        </select>
                    </td>
                `;
                ordersTableBody.appendChild(row);
                console.log(order.estimated_delivery)
            });

            // Reapply the status change restrictions
            restrictStatusChanges();
        })
        .catch(error => console.error('Error refreshing orders:', error));
}

// Run the restrictStatusChanges function on page load to apply the restrictions
document.addEventListener('DOMContentLoaded', restrictStatusChanges);
