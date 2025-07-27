document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');
  const errorMessage = document.getElementById('error-message');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorMessage.textContent = '';

    const email = form.email.value.trim();
    const password = form.password.value;

    try {
      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Login failed');
      }

      const data = await response.json();

      // Save token to localStorage (or cookie)
      localStorage.setItem('jwt_token', data.access_token);

      // Redirect to index page after login
      window.location.href = 'index.html';
    } catch (err) {
      errorMessage.textContent = err.message;
    }
  });
});
