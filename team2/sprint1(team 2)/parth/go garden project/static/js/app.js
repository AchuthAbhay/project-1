document.addEventListener('DOMContentLoaded', () => {
    fetch('https://jsonplaceholder.typicode.com/posts')  // Replace with your API
        .then(response => response.json())
        .then(products => {
            const productsContainer = document.getElementById('products-container');
            products.forEach(product => {
                const productCard = document.createElement('div');
                productCard.classList.add('product-card');
                productCard.innerHTML = `
                    <img src="https://via.placeholder.com/150" alt="${product.title}" class="product-image">
                    <h2 class="product-name">${product.title}</h2>
                    <p class="product-price">$${(Math.random() * 100).toFixed(2)}</p>
                    <a href="product-details.html?id=${product.id}" class="view-details">View Details</a>
                `;
                productsContainer.appendChild(productCard);
            });
        })
        .catch(error => console.error('Error fetching products:', error));
});
