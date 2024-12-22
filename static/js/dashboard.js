// Function to generate random colors for each bar
function getRandomColor(count) {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

// Function to fetch the total sales 
function getTotalSales() {
    fetch('/api/total_sales')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch total sales data');
            }
            return response.json(); 
        })
        .then(data => {
            const totalSales = data.total_sales;
            document.getElementById('sales').innerText = totalSales;
            console.log('Formatted Total Sales:', totalSales);
        })
        .catch(error => {
            console.error('Error fetching total sales:', error);
        });
}

// Function to fetch the total profit 
function getTotalProfit() {
    fetch('/api/total_profit')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch total profit data');
            }
            return response.json(); 
        })
        .then(data => {
            const totalProfit = data.total_profit;
            document.getElementById('profit').innerText = totalProfit;
        })
        .catch(error => {
            console.error('Error fetching total Profit:', error);
        });
}

// Function to fetch the average order price 
function getAverageOrderPrice() {
    fetch('/api/average_order_price')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch average order price data');
            }
            return response.json(); 
        })
        .then(data => {
            const totalProfit = data.average_order_price;
            document.getElementById('average').innerText = totalProfit;
        })
        .catch(error => {
            console.error('Error fetching average order price:', error);
        });
}

// Fetch product availability and render chart
function getProductAvailability(val) {
    fetch('/api/product_availability')
        .then(response => response.json())
        .then(data => {
            let labels = data.map(item => item.product);
            let values = data.map(item => item.availability_count);
            // Generate a unique color for each bar
            let colors = values.map(() => getRandomColor(values.length));

            new Chart("productAvailability", {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{
                        backgroundColor: colors,
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
            // Generate a unique color for each bar
            let colors = values.map(() => getRandomColor(values.length));

            new Chart("totalProductsSold", {
                type: "doughnut",
                data: {
                    labels: labels,
                    datasets: [{
                        backgroundColor: colors,
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
                type: "line",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Total Sales",
                        backgroundColor: "rgba(255, 159, 64,0.4)",
                        borderColor:"rgba(255, 159, 64,1)",
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
            // Generate a unique color for each bar
            let colors = values.map(() => getRandomColor(values.length));
            console.log(colors)

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
                    title: {
                        display: true,
                        text: "Top Performing Products"
                    },
                    scales: {
                        y: {
                            min: 0,
                            ticks: {
                                stepSize: 5 // Adjust step size if needed
                            }
                        }
                    }
                }
            });
        });
}

let userChart;
function usersLocation(location) {
    if (location == "" || location == undefined || location == null) {
        location = "country";
    }
    fetch(`/api/customers/location?location=${location}`)
        .then(response => response.json())
        .then(data => {
            let labels = data.map(item => item.location);
            let values = data.map(item => item.user_count);
            // Generate a unique color for each bar
            let colors = values.map(() => getRandomColor(values.length));

            if (userChart) {
                // Update the existing chart instance
                userChart.data.labels = labels;
                userChart.data.datasets[0].data = values;
                userChart.data.datasets[0].backgroundColor = colors;
                userChart.update(); // Refresh the chart with new data
            } else {
                // Create the chart instance if it doesn't exist
                userChart = new Chart("userslocation", {
                    type: "pie",
                    data: {
                        labels: labels,
                        datasets: [{
                            label: "User Location",
                            backgroundColor: colors,
                            data: values
                        }]
                    },
                    options: {
                        plugins: {
                            title: {
                                display: true,
                                text: "Product Sold (Count)"
                            }
                        }
                    }
                });
            }
        });
}

let trendChart;
function trendingProducts(season) {
    // Fetch the data based on the season
    fetch(`/api/sales/season?season=${season}`)
        .then(response => response.json())
        .then(data => {
            let labels = data.map(item => item.product_name);
            let values = data.map(item => item.total_sales);
            // Generate a unique color for each bar
            let colors = values.map(() => getRandomColor(values.length));

            if (trendChart) {
                // Update the existing chart instance
                trendChart.data.labels = labels;
                trendChart.data.datasets[0].data = values;
                trendChart.data.datasets[0].backgroundColor = colors;
                trendChart.update(); // Refresh the chart with new data
            } else {
                // Create the chart instance if it doesn't exist
                trendChart = new Chart("trendingproducts", {
                    type: "bar",
                    data: {
                        labels: labels,
                        datasets: [{
                            label: "Trending",
                            backgroundColor: colors,
                            data: values
                        }]
                    },
                    options: {
                        plugins: {
                            title: {
                                display: true,
                                text: "Product Sold (Count)"
                            }
                        }
                    }
                });
            }
        })
        .catch(error => console.error("Error fetching data:", error));
}

// Function to fetch the repeat customer rate 
function repeatCustomerRate() {
    fetch('/api/repeat_customer_rate')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch average order price data');
            }
            return response.json(); 
        })
        .then(data => {
            const totalProfit = data.repeat_customer_rate;
            document.getElementById('repeat_customer_rate').innerText = totalProfit;
        })
        .catch(error => {
            console.error('Error fetching average order price:', error);
        });
}

// Fetch repeat customer rate and render line chart
function repeatCustomers() {
    fetch('/api/monthly_customer_counts')
        .then(response => response.json())
        .then(data => {
            let labels = data.map(item => item.month);
            let values1 = data.map(item => item.new_customers);
            let values2 = data.map(item => item.old_Customers);
            console.log(values2);
            new Chart("repeat", {
                type: "line", 
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Repeat Customers',
                        data: values2,
                        borderColor: "red",
                        fill: false
                      },{
                        label: 'New Customers',
                        data: values1,
                        borderColor: "green",
                        fill: false
                      },

                 ]
                  
                },
                options: {
                    title: {
                        display: true,
                        
                    }
                }
            });
        });
}


function  deliveryPerformance() {
    fetch('/api/delivery_performance')
        .then(response => response.json())
        .then(data => {
            let labels = data.map(item => item.delivery_type);
            let values = data.map(item => item.count);
            // Generate a unique color for each bar
            let colors = values.map(() => getRandomColor(values.length));

            new Chart("deliveryperformance", {
                type: "doughnut",
                data: {
                    labels: labels,
                    datasets: [{
                        backgroundColor: colors,
                        data: values
                    }]
                },
                options: {
                    title: {
                        display: true,
                        text: ""
                    }
                }
            });
        });
}


// Initialize all charts on window load
window.onload = () => {
    getTotalSales();
    getTotalProfit();
    getAverageOrderPrice();
    getProductAvailability();
    getTotalProductsSold();
    profitChart();
    salesPerformance();
    topPerformingProducts();
    usersLocation();
    trendingProducts("all");
    repeatCustomerRate();
    repeatCustomers(); 
   deliveryPerformance();
};
