#   InkDash
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
> Este é um sistema de gerenciamento interno para estúdios de tatuagem. Nele é possível gerenciar agendamentos, clientes, usuários e materiais.

### Ajustes e melhorias

O projeto ainda está em desenvolvimento e as próximas atualizações serão voltadas nas seguintes tarefas:

- [ ] Agendamentos (CRUD)

## 🚀 Instalando a InkDash

Para instalar a Inkdash, siga estas etapas:

1. Após clonar os arquivos em sua máquina, abra o terminal.
2. Utilize os seguintes comandos para baixar as dependências.

```bash
pip install -r requirements.txt
python -m venv fastapi_env
install fastapi uvicorn
```
> [!NOTE]
> É possível utilizar outro nome ao invés de "fastapi_env".

3. Instale a entensão do MongoDB no vscode

## ☕ Inicializando a Inkdash

1. Abra um terminal específico para cada serviço do sistema (6 no total)

2. Em cada terminal aberto inicialize o fastapi

```bash
fastapi_env\Scripts\activate
```
> [!WARNING]
> Caso tenha mudado o nome da pasta ao baixar as depêndencias utilize o novo nome ao invés de "fastapi_env".

3. Digite cada comando a seguir num terminal diferente.

```bash
uvicorn routes.loginRoute:app --reload --port 8000
uvicorn routes.userRoute:app --reload --port 8001
uvicorn routes.redefinicaoRoute:app --reload --port 8002
uvicorn routes.clienteRoute:app --reload --port 8003
uvicorn routes.materialRoute:app --reload --port 8004
uvicorn routes.agendaRoute:app --reload --port 8004

```
### Inicializando o Banco

1. Para o banco de dados inicie o MongoDB na seginte porta:

```bash
mongodb://localhost:27017
```
2. Crie um banco chamando "streetwise_db"
3. Dentro do banco crie as collection: "users", "agendamentos", "cliente" e "material"

> [!TIP]
> Você pode utilizar as rotas tanto usando o nosso front-end quando utilizado alguma extensão como postman ou thunder

## 🤝 Colaboradores

<table>
  <tr>
    <td align="center">
      <a href="#" title="defina o titulo do link">
        <img src="https://avatars.githubusercontent.com/u/128440479?s=400&u=a308ecb320d3bc000c31194508b884eadbb01366&v=4" width="100px;" alt="Foto do Brielalmeida no GitHub"/><br>
        <sub>
          <b>Brielalmeida</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="defina o titulo do link">
        <img src="https://avatars.githubusercontent.com/u/99226416?v=4" width="100px;" alt="Foto do João Pedro de Lima"/><br>
        <sub>
          <b>João Pedro de Lima</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="defina o titulo do link">
        <img src="https://avatars.githubusercontent.com/u/116198015?v=4" width="100px;" alt="Foto do Kaunang"/><br>
        <sub>
          <b>Kauang☯</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="defina o titulo do link">
        <img src="https://avatars.githubusercontent.com/u/107219109?v=4" width="100px;" alt="Foto do Hideaki Fukami"/><br>
        <sub>
          <b>Hideaki Fukami</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="defina o titulo do link">
        <img src="https://avatars.githubusercontent.com/u/131377083?v=4" width="100px;" alt="Foto do HenryPilotinho"/><br>
        <sub>
          <b>HenryPilotinho</b>
        </sub>
      </a>
    </td>
  </tr>
</table>