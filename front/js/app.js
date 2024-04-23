import FetchService from './Components/FetchService.js';
import PasswordRecovery from './Components/PasswordRecovery.js';
import Login from './Components/Login.js'

class App {
    constructor(apiBaseUrl) {
        this.apiBaseUrl = apiBaseUrl;
        this.appElement = document.getElementById('app');
        this.fetchService = new FetchService(this.apiBaseUrl);
        this.initApp();
    }

    initApp() {
        this.login = new Login(this.fetchService, () => this.fetchItems());
        this.PasswordRecovery = new PasswordRecovery(this.fetchService, () => this.fetchItems());
        this.appElement.innerHTML = `
        <div class="panel">
            <div id="login"></div>
            <div id="PasswordRecovery"></div>
        </div>
        `;

        this.render('login', this.login.render());
        this.login.afterRender();

        this.afterRender();

    }

    render(elementId, html) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = html;
        }
    }

    async afterRender() {
        document.getElementById('esqueceu').addEventListener('submit', (e) => PasswordRec.openModal(e));
    }
    


}

const apiBaseUrl = 'http://127.0.0.1:8001';
const app = new App(apiBaseUrl);