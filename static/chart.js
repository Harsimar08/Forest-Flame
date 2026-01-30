const ctx = document.getElementById('fireChart').getContext('2d');

new Chart(ctx, {
    type: 'bar',
    data: {
        labels: chartLabels,
        datasets: [{
            label: 'Fire Risk Level',
            data: chartData,
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 1
                }
            }
        }
    }
});
