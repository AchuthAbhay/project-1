
document.addEventListener('DOMContentLoaded', () => {
    // Categories
    const categories = {
      "flower-seeds": document.getElementById('flower-seeds-list'),
      "flower-bulbs": document.getElementById('flower-bulbs-list'),
      "garden-essentials": document.getElementById('garden-essentials-list'),
      "veg-seeds": document.getElementById('veg-seeds-list'),
      "gift-cards": document.getElementById('gift-cards-list')
    };
  
    // Example product data (You would replace this with a real API call)
    const products = [
      { id: 1, name: "Rose Seed", price: 10, category: "flower-seeds", imageUrl: "https://via.placeholder.com/200" },
      { id: 2, name: "Tulip Bulb", price: 12, category: "flower-bulbs", imageUrl: "https://via.placeholder.com/200" },
      { id: 3, name: "Garden Tools Set", price: 30, category: "garden-essentials", imageUrl: "https://via.placeholder.com/200" },
      { id: 4, name: "Tomato Seed", price: 5, category: "veg-seeds", imageUrl: "https://via.placeholder.com/200" },
      { id: 5, name: "Gift Card $50", price: 50, category: "gift-cards", imageUrl: "https://via.placeholder.com/200" },
    ];
  
    // Loop through each product and categorize it
    products.forEach(product => {
      const productCard = document.createElement('div');
      productCard.classList.add('product-card');
      productCard.innerHTML = `
        <img src="${product.imageUrl}" alt="${product.name}" class="product-image">
        <h3 class="product-title">${product.name}</h3>
        <p class="product-price">$${product.price}</p>
        <a href="/products/${product.id}" class="product-details-link">View Details</a>
      `;
      
      // Append the product to the appropriate category section
      const categoryElement = categories[product.category];
      if (categoryElement) {
        categoryElement.appendChild(productCard);
      }
    });
  });
  