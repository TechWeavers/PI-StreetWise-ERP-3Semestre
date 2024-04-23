import PasswordRecovery from './PasswordRecovery.js';

class Login {
    constructor(fetchService, renderCallback) {
        this.fetchService = fetchService;
        this.renderApp = renderCallback;
        this.passwordRecovery = new PasswordRecovery(this.fetchService, () => this.fetchItems());
    }

    render() {
        return `
            <div class="telaLogin">
                <h2>Login</h2>
                <form id="login-form" action="/login" method="post">
                    <input type="text" id="username" placeholder="Usuário" required>
                    <input type="password" id="password" placeholder="Senha" required>
                    <button type="submit">Entrar</button>
                </form>
                <button class="rec" id="esqueceu" type="button">Esqueceu a senha?</button>
            </div>
            <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }

            .rec{
                margin-top: 5px;
            }
            
            .login-container {
                background-color: #fff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                width: 300px;
                text-align: center;
            }
            
            h2 {
                margin-bottom: 20px;
            }
            
            input[type="text"],
            input[type="password"] {
                width: calc(100% - 20px);
                padding: 10px;
                margin: 5px 0 15px 0;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            
            button {
                background-color: #007bff;
                color: #fff;
                border: none;
                border-radius: 3px;
                padding: 10px 20px;
                cursor: pointer;
            }
            
            button:hover {
                background-color: #0056b3;
            }

            
            </style>
            
        `;
    }

    afterRender() {
        document.getElementById('esqueceu').addEventListener('click', () => this.openModal()); 
        document.getElementById('login-form').addEventListener('submit', (e) => this.login(e));
    }

    openModal() {
        this.passwordRecovery.openModal();
    }

    async login(event) {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        if (!username || !password) {
            alert('Campos vazios');
            return; // Adicionado para evitar a execução adicional do código
        }

        await this.fetchService.fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({username, password}),
        });

    }
}
export default Login;