document.addEventListener('DOMContentLoaded', () => {
    const searchBar = document.getElementById('search-bar');
    const productGrid = document.querySelector('.product-grid');
    const filterForm = document.querySelector('.filter-form');

    // Event listener for keyup on search bar
    searchBar.addEventListener('keyup', async () => {
        const formData = new FormData(filterForm); // Gather form data
        const queryString = new URLSearchParams(formData).toString(); // Convert to query string

        try {
            const response = await fetch(`${filterForm.action}?${queryString}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const html = await response.text();
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newProductGrid = doc.querySelector('.product-grid');
                productGrid.innerHTML = newProductGrid.innerHTML; // Update the product grid
            } else {
                console.error('Failed to fetch products:', response.status);
            }
        } catch (error) {
            console.error('Error fetching products:', error);
        }
    });
});











