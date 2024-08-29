document.addEventListener("DOMContentLoaded", function() {
    const labels = {{ labels | safe }};
    const data = {
        labels: labels,
        datasets: [
            {% for veg, prices in price_fluctuation.items() %}
            {
                label: '{{ veg }}',
                data: {{ prices | safe }},
                borderColor: getRandomColor(),
                fill: false
            },
            {% endfor %}
        ]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Price'
                    }
                }
            }
        }
    };

    new Chart(
        document.getElementById('price-fluctuation-chart'),
        config
    );

    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }
});
