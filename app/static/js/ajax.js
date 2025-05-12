// app/static/js/ajax.js
document.addEventListener('DOMContentLoaded', () => {
    // Gestion des likes
    const likeButtons = document.querySelectorAll('.like-button');
    likeButtons.forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();
            const artworkId = button.dataset.artworkId;
            try {
                const response = await fetch(`/interactions/like/${artworkId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content
                    }
                });
                const data = await response.json();
                if (data.success) {
                    button.textContent = `❤️ ${data.likes_count}`;
                } else {
                    alert('Erreur lors du like.');
                }
            } catch (error) {
                console.error('Erreur:', error);
                alert('Une erreur est survenue.');
            }
        });
    });

    // Charger les commentaires dynamiquement
    const commentForms = document.querySelectorAll('.comment-form');
    commentForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const artworkId = form.dataset.artworkId;
            const commentText = form.querySelector('.comment-input').value;
            try {
                const response = await fetch(`/interactions/comment/${artworkId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content
                    },
                    body: JSON.stringify({ comment: commentText })
                });
                const data = await response.json();
                if (data.success) {
                    const commentSection = document.querySelector(`#comments-${artworkId}`);
                    const newComment = document.createElement('div');
                    newComment.textContent = `${data.username}: ${commentText}`;
                    commentSection.appendChild(newComment);
                    form.reset();
                } else {
                    alert('Erreur lors de l\'ajout du commentaire.');
                }
            } catch (error) {
                console.error('Erreur:', error);
                alert('Une erreur est survenue.');
            }
        });
    });
});