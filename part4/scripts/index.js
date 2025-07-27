document.addEventListener("DOMContentLoaded", () => {
  const token = getToken();
  if (!token) {
    window.location.href = "login.html";
    return;
  }

  fetchPlaces();
});

function getToken() {
  const match = document.cookie.match(new RegExp("(^| )token=([^;]+)"));
  return match ? match[2] : null;
}

function fetchPlaces() {
  fetch("http://localhost:5000/api/v1/places", {
    headers: {
      Authorization: `Bearer ${getToken()}`
    }
  })
    .then(response => {
      if (!response.ok) throw new Error("Failed to fetch places");
      return response.json();
    })
    .then(data => {
      populatePlaces(data);
      populatePriceFilter(data);
    })
    .catch(error => {
      console.error(error);
      alert("Error loading places.");
    });
}

function populatePlaces(places) {
  const placesList = document.getElementById("places-list");
  placesList.innerHTML = "";

  places.forEach(place => {
    const card = document.createElement("div");
    card.className = "place-card";
    card.innerHTML = `
      <h3>${place.name}</h3>
      <p>Price per night: $${place.price_per_night}</p>
      <button class="details-button" data-id="${place.id}">View Details</button>
    `;
    placesList.appendChild(card);
  });

  document.querySelectorAll(".details-button").forEach(button => {
    button.addEventListener("click", () => {
      const placeId = button.getAttribute("data-id");
      window.location.href = `place.html?id=${placeId}`;
    });
  });
}

function populatePriceFilter(places) {
  const prices = [...new Set(places.map(p => p.price_per_night))].sort((a, b) => a - b);
  const priceSelect = document.getElementById("price-filter");
  priceSelect.innerHTML = `<option value="">All Prices</option>`;
  prices.forEach(price => {
    const option = document.createElement("option");
    option.value = price;
    option.textContent = `$${price}`;
    priceSelect.appendChild(option);
  });

  priceSelect.addEventListener("change", () => {
    const selectedPrice = priceSelect.value;
    const filtered = selectedPrice
      ? places.filter(p => p.price_per_night == selectedPrice)
      : places;
    populatePlaces(filtered);
  });
}
