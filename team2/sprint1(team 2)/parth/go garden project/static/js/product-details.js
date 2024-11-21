document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');

    if (productId) {
        fetch(`https://jsonplaceholder.typicode.com/posts/${productId}`)  // Replace with your API
            .then(response => response.json())
            .then(product => {
                const productDetailContainer = document.getElementById('product-detail-container');
                productDetailContainer.innerHTML = `
                    <img src="https://via.placeholder.com/500" alt="${product.title}" class="product-detail-image">
                    <h2 class="product-detail-name">${product.title}</h2>
                    <p class="product-detail-price">$${(Math.random() * 100).toFixed(2)}</p>
                    <p class="product-detail-description">${product.body}</p>
                    <button class="buy-now">Buy Now</button>
                `;
            })
            .catch(error => console.error('Error fetching product details:', error));
    }
});
