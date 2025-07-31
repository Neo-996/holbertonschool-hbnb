document.addEventListener('DOMContentLoaded', () => {
  function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [key, value] = cookie.trim().split('=');
      if (key === name) return value;
    }
    return null;
  }

  const token = getCookie('token');
  const params = new URLSearchParams(window.location.search);
  const placeId = params.get('place_id');

  // Redirect to login if no token
  if (!token) {
    window.location.href = 'login.html';
    return;
  }

  // Redirect to index if no place ID
  if (!placeId) {
    alert('No place specified for review.');
    window.location.href = 'index.html';
    return;
  }

  const form = document.getElementById('review-form');
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const rating = form.rating.value;
    const comment = form.comment.value.trim();

    if (rating < 1 || rating > 5 || !comment) {
      alert('Please enter a valid rating (1–5) and a comment.');
      return;
    }

    try {
      const response = await fetch('/api/v1/reviews', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          place_id: placeId,
          rating: parseInt(rating),
          comment: comment
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to submit review.');
      }

      alert('Review submitted successfully!');
      window.location.href = `place.html?id=${placeId}`;
    } catch (error) {
      alert(`Error: ${error.message}`);
    }
  });
});

