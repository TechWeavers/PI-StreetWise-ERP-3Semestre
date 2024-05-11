class PasswordRecovery {
    constructor(fetchService, renderCallback, openModalCallback) {
        this.fetchService = fetchService;
        this.renderApp = renderCallback;
        this.modalCallback = openModalCallback;
    }

    render() {
        return `
        <div class="recuperarCard" id="recuperarCard">
            <h2>Email</h2>
            <form id="email-form" action="/recuperarSenha" method="post">
                <input type="email" name="email" placeholder="Digite seu email" required>
                <button type="submit">Enviar</button>
            </form>
        </div>
        <style>
            .recuperarCard {
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                overflow: auto;
                background-color: rgba(0, 0, 0, 0.5);
                backdrop-filter: blur(25px);
                border: solid 2px blueviolet;
            }
        </style>
      `;
    }

    openModal() {
        const modal = document.querySelector('.recuperarCard');
        if (modal) {
            modal.style.display = 'block';
        } else {
            console.error("Elemento com a classe 'recuperarCard' não encontrado.");
        }
    }

    closeModal() {
        const modal = document.querySelector('.recuperarCard');
        modal.style.display = 'none';
    }
    
    afterRender() {
        document.getElementById('email-form').addEventListener('submit', (event) => {
            event.preventDefault();
            this.recuperarSenha();
        });
    }

    async recuperarSenha() {
        const email = document.querySelector('input[name="email"]').value;

        await this.fetchService.fetch(`/recuperarSenha`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email }),
        });

        alert('Solicitação de recuperação de senha enviada com sucesso.');
        this.closeModal();
        this.renderApp();
    }
}
export default PasswordRecovery;