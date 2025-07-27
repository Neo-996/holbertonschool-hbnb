document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();
      const errorMsg = document.getElementById('error-message');

      try {
        const response = await fetch('http://localhost:5000/api/v1/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Login failed');
        }

        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;

        window.location.href = 'index.html';
      } catch (error) {
        if (errorMsg) {
          errorMsg.textContent = error.message;
        } else {
          alert(error.message);
        }
      }
    });
  }
});
