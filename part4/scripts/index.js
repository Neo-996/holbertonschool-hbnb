document.addEventListener('DOMContentLoaded', () => {
  const token = localStorage.getItem('jwt_token');

  // Redirect to login if not authenticated
  if (!token) {
    window.location.href = 'login.html';
    return;
  }

  const placesList = document.getElementById('places-list');
  const countryFilter = document.getElementById('country-filter');
  let allPlaces = [];

  // Fetch places from API
  async function fetchPlaces() {
    try {
      const response = await fetch('/api/v1/places', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch places');
      }

      allPlaces = await response.json();
      populateCountryFilter(allPlaces);
      displayPlaces(allPlaces);
    } catch (error) {
      placesList.innerHTML = `<p style="color:red;">${error.message}</p>`;
    }
  }

  // Populate country dropdown filter options
  function populateCountryFilter(places) {
    // Clear existing options except 'All'
    countryFilter.innerHTML = '<option value="all">All Countries</option>';

    const countries = [...new Set(places.map(p => p.country).filter(Boolean))].sort();
    countries.forEach(country => {
      const option = document.createElement('option');
      option.value = country;
      option.textContent = country;
      countryFilter.appendChild(option);
    });
  }

  // Display places on the page
  function displayPlaces(places) {
    placesList.innerHTML = '';
    if (places.length === 0) {
      placesList.innerHTML = '<p>No places found.</p>';
      return;
    }
    places.forEach(place => {
      const card = document.createElement('div');
      card.className = 'place-card';
      card.innerHTML = `
        <h3>${place.title}</h3>
        <p>Price per night: $${place.price_per_night}</p>
        <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
      `;
      placesList.appendChild(card);
    });
  }

  // Event listener for country filter change
  countryFilter.addEventListener('change', () => {
    const selectedCountry = countryFilter.value;
    if (selectedCountry === 'all') {
      displayPlaces(allPlaces);
    } else {
      const filtered = allPlaces.filter(place => place.country === selectedCountry);
      displayPlaces(filtered);
    }
  });

  fetchPlaces();
});
