document.addEventListener('DOMContentLoaded', async () => {
  function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [key, value] = cookie.trim().split('=');
      if (key === name) return value;
    }
    return null;
  }

  const params = new URLSearchParams(window.location.search);
  const placeId = params.get('id');
  const token = getCookie('token');
  const addReviewBtn = document.getElementById('add-review-btn');

  if (!token) {
    window.location.href = 'login.html';
    return;
  }

  if (!placeId) {
    alert('No place ID specified');
    window.location.href = 'index.html';
    return;
  }

  try {
    const res = await fetch(`/api/v1/places/${placeId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!res.ok) {
      throw new Error('Failed to load place details');
    }

    const place = await res.json();

    document.getElementById('place-title').textContent = place.title;
    document.getElementById('place-host').textContent = `Host: ${place.owner.first_name} ${place.owner.last_name}`;
    document.getElementById('place-price').textContent = `Price per night: $${place.price_per_night}`;
    document.getElementById('place-description').textContent = place.description;

    const amenitiesList = document.getElementById('amenities-list');
    amenitiesList.innerHTML = '';
    if (place.amenities && place.amenities.length > 0) {
      place.amenities.forEach(amenity => {
        const li = document.createElement('li');
        li.textContent = amenity.name;
        amenitiesList.appendChild(li);
      });
    } else {
      amenitiesList.innerHTML = '<li>No amenities listed</li>';
    }

    const reviewsList = document.getElementById('reviews-list');
    reviewsList.innerHTML = '';
    if (place.reviews && place.reviews.length > 0) {
      place.reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        reviewCard.innerHTML = `
          <p>"${review.comment}"</p>
          <p>By: ${review.user.first_name} ${review.user.last_name}</p>
          <p>Rating: ${review.rating}/5</p>
        `;
        reviewsList.appendChild(reviewCard);
      });
    } else {
      reviewsList.innerHTML = '<p>No reviews yet.</p>';
    }

    addReviewBtn.style.display = 'inline-block';
    addReviewBtn.addEventListener('click', () => {
      window.location.href = `add_review.html?place_id=${placeId}`;
    });

  } catch (error) {
    alert(error.message);
    window.location.href = 'index.html';
  }
});

