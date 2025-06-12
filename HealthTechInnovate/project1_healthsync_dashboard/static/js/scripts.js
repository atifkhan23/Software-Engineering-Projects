async function fetchVitalsData() {
    try {
        const response = await fetch('/api/vitals');
        const vitals = await response.json();
        const labels = vitals.map(v => new Date(v.date).toLocaleDateString());
        const weights = vitals.map(v => v.weight);
        const ctx = document.getElementById('vitalsChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Weight (kg)',
                    data: weights,
                    borderColor: '#007bff',
                    fill: false
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: { title: { display: true, text: 'Date' } },
                    y: { title: { display: true, text: 'Weight (kg)' } }
                }
            }
        });
    } catch (error) {
        console.error('Error fetching vitals:', error);
    }
}