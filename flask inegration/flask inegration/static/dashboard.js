// Fetch product availability and render chart
function getProductAvailability(val) {
    fetch('/api/product_availability')
        .then(response => response.json())
        .then(data => {
            let labels = data.map(item => item.product);
            let values = data.map(item => item.availability_count);
            new Chart("productAvailability", {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{
                        backgroundColor: ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9"],
                        data: values
                    }]
                },
                options: {
                    title: {
                        display: true,
                        text: "Product Availability (Count)"
                    }
                }
            });
        });
}

// Fetch total products sold by category and render chart
function getTotalProductsSold() {
    fetch('/api/total_sales_by_category')
        .then(response => response.json())
        .then(data => {
            let labels = data.map(item => item.category);
            let values = data.map(item => item.total_sales);
            new Chart("totalProductsSold", {
                type: "doughnut",
                data: {
                    labels: labels,
                    datasets: [{
                        backgroundColor: ["#ff6384", "#36a2eb", "#ffcd56", "#4bc0c0"],
                        data: values
                    }]
                },
                options: {
                    title: {
                        display: true,
                        text: "Total Products Sold by Category"
                    }
                }
            });
        });
}

// Fetch profit data and render chart
function profitChart() {
    fetch('/api/daily_profit')
        .then(response => response.json())
        .then(data => {
            let labels = data.map(item => item.date);
            let values = data.map(item => item.daily_profit);
            new Chart("profitChart", {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Profit",
                        backgroundColor: "rgba(75,192,192,0.4)",
                        borderColor: "rgba(75,192,192,1)",
                        data: values,
                        fill: true
                    }]
                },
                options: {
                    title: {
                        display: true,
                        text: "Profit Over Periods"
                    }
                }
            });
        });
}

// Fetch sales performance data and render chart
function salesPerformance() {
    fetch('/api/daily_sales')
        .then(response => response.json())
        .then(data => {
            let labels = data.map(item => item.sale_date);
            let values = data.map(item => item.total_sales);
            new Chart("salesPerformance", {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Total Sales",
                        backgroundColor: "#ff9f40",
                        data: values
                    }]
                },
                options: {
                    title: {
                        display: true,
                        text: "Sales Performance Over Periods"
                    }
                }
            });
        });
}

// Fetch Top Performing Products and render chart
function topPerformingProducts() {
    fetch('/api/top_performing_products')
        .then(response => response.json())
        .then(data => {
            let labels = data.map(item => item.product_name);
            let values = data.map(item => item.total_sales);

            // Function to generate random colors for each bar
            function getRandomColor() {
                const letters = '0123456789ABCDEF';
                let color = '#';
                for (let i = 0; i < 6; i++) {
                    color += letters[Math.floor(Math.random() * 16)];
                }
                return color;
            }

            // Generate a unique color for each bar
            let colors = values.map(() => getRandomColor());

            new Chart("topPerformingProducts", {
                type: "bar", 
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Top Sales",
                        backgroundColor: colors,  // Assign random colors to each bar
                        data: values
                    }]
                },
                options: {
                    indexAxis: 'x',  // Set the chart to be horizontal
                    title: {
                        display: true,
                        text: "Top Performing Products"
                    }
                }
            });
        });
}


// Initialize all charts on window load
window.onload = () => {
    getProductAvailability();
    getTotalProductsSold();
    profitChart();
    salesPerformance();
    topPerformingProducts();
};
