// app/static/js/charts.js
import Chart from 'chart.js/auto';

document.addEventListener('DOMContentLoaded', async () => {
    const ctx = document.getElementById('engagementChart')?.getContext('2d');
    if (!ctx) return;

    try {
        // Récupérer les données via une requête AJAX
        const response = await fetch('/admin/statistics', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();

        // Créer un graphique avec Chart.js
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels, // ex. ['Janvier', 'Février', ...]
                datasets: [{
                    label: 'Likes',
                    data: data.likes, // ex. [10, 20, 30, ...]
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }, {
                    label: 'Commentaires',
                    data: data.comments, // ex. [5, 15, 25, ...]
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
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
    } catch (error) {
        console.error('Erreur lors du chargement des données:', error);
    }
});