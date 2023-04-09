const ctx = document.getElementById('myChart');

new Chart(ctx, {
    type: 'bar',
    data: {
        labels: {{ monthNumber | safe}},
    datasets: [{
        label: 'Orders By Month',
        data: {{ totalOrders }},
    borderWidth: 1
        }]
    },
    options: {
    scales: {
        y: {
            beginAtZero: true
        }
    }
}
});