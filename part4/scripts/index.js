document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault(); // Prevent default form submission

      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();

      try {
        // Send login request to the API
        const response = await fetch('http://localhost:5000/api/v1/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
        });

        // If login fails, show the error message
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Login failed');
        }

        // On success, store the JWT token in cookies
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;

        // Redirect to the main page
        window.location.href = 'index.html';
      } catch (error) {
        // Display error message in the designated element or alert fallback
        const errorMsg = document.getElementById('error-message');
        if (errorMsg) {
          errorMsg.textContent = error.message;
        } else {
          alert(error.message);
        }
      }
    });
  }
});

