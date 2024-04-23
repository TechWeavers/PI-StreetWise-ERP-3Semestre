import FetchService from './Components/FetchService.js';
import ItemForm from './Components/ItemForm.js';
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
        this.appElement.innerHTML = `
        <div class="panel">
            <div id="login"></div>
        </div>
        `;

        this.render('login', this.login.render());
        this.login.afterRender();
    }

    dadosLogin(login) {
        document.getElementById('username').value = login.username;
        document.getElementById('password').value = login.password;
    }

    render(elementId, html) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = html;
        }
    }



}

const apiBaseUrl = 'http://127.0.0.1:8000';
const app = new App(apiBaseUrl);