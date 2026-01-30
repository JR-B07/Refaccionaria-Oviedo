// Login JavaScript - FALAF ERP

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const messageDiv = document.getElementById('message');
    const enterBtn = loginForm.querySelector('.btn-enter');

    // Submit form
    loginForm.addEventListener('submit', handleLogin);

    // Enter key on password field
    passwordInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleLogin(e);
        }
    });

    // Clear message on input
    usernameInput.addEventListener('input', () => clearMessage());
    passwordInput.addEventListener('input', () => clearMessage());

    async function handleLogin(e) {
        e.preventDefault();

        const username = usernameInput.value.trim();
        const password = passwordInput.value;

        // Validar campos
        if (!username) {
            showMessage('Por favor ingresa tu usuario', 'error');
            usernameInput.focus();
            return;
        }

        if (!password) {
            showMessage('Por favor ingresa tu contraseña', 'error');
            passwordInput.focus();
            return;
        }

        // Desactivar botón durante envío
        enterBtn.disabled = true;
        enterBtn.textContent = 'AUTENTICANDO...';
        showMessage('Procesando...', 'info');

        try {
            const response = await fetch('/api/v1/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Login exitoso
                showMessage('¡Acceso concedido! Redirigiendo...', 'success');

                // Guardar token y datos del usuario en localStorage
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('token_type', data.token_type);
                localStorage.setItem('user', JSON.stringify(data.user));

                // Guardar información de sucursal
                if (data.user.local_id) {
                    localStorage.setItem('sucursal_id', data.user.local_id);
                    localStorage.setItem('sucursal_nombre', data.user.local_nombre || 'Sucursal');
                    localStorage.setItem('nombre_usuario', data.user.name || data.user.username);
                }

                // Debug: verificar que se guardó
                console.log('✅ Token guardado:', localStorage.getItem('access_token'));
                console.log('✅ Sucursal:', localStorage.getItem('sucursal_nombre'));

                // Redirigir al dashboard (ajusta la URL según tu estructura)
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 500);
            } else {
                // Error de autenticación
                const errorMsg = data.detail || data.message || 'Usuario o contraseña incorrectos';
                showMessage(errorMsg, 'error');
                passwordInput.value = '';
                passwordInput.focus();
            }
        } catch (error) {
            console.error('Error en login:', error);
            showMessage('Error de conexión. Intenta nuevamente.', 'error');
        } finally {
            // Reactivar botón
            enterBtn.disabled = false;
            enterBtn.textContent = 'ENTRAR';
        }
    }

    function showMessage(text, type = 'info') {
        messageDiv.textContent = text;
        messageDiv.className = `message show ${type}`;
    }

    function clearMessage() {
        messageDiv.className = 'message hidden';
        messageDiv.textContent = '';
    }

    // Auto-focus en username al cargar
    usernameInput.focus();
});
