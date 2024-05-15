#   InkDash

<img src="imagem.png" alt="Exemplo imagem">

> Este é um sistema de gerenciamento interno para estúdios de tatuagem. Nele é possível gerenciar agendamentos, clientes, usuários e materiais.

### Ajustes e melhorias

O projeto ainda está em desenvolvimento e as próximas atualizações serão voltadas nas seguintes tarefas:

- [ ] Agendamentos (CRUD)

## 🚀 Instalando a InkDash

Para instalar a Inkdash, siga estas etapas:

1. Após clonar os arquivos em sua máquina, abra o terminal.
2. Utilize os seguintes comandos para baixar as dependências

```bash
pip install -r requirements.txt
python -m venv fastapi_env
install fastapi uvicorn
```
> [!NOTE]
> É possível utilizar outro nome ao invés de "fastapi_env".

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








Este é um projeto de um sistema de gerenciamento para estúdios de tatuagem feito com Python (FastAPI) e Javascript (React), utilizando banco de dados não-relacional, e arquitetura orientada a microsserviços
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
O projeto contém uma arquitetura orientada a serviços, que possui uma estrutura front-end em formato de SPA (Single Page Applications) localizada na pasta "front" (apenas de teste) que enviará requisições para os serviços no back-end.

Configs: Pasta com arquivo que faz conexão com banco de dados MongoDB

Controllers: Arquivos de controle que serão chamados dentro das rotas de aplicação, contém a lógica de negócio de cada solicitação 

crud_mongo: Gerenciamento do pacote virtual 

front: contém arquivos de desenvolvimento front-end, em formato SPA (Single Page Application), que enviarão as requisições para o servidor via fetch

models: arquivos de validação dos dados que serão enviados nas requisições, garantem que os dados enviados estejam dentro de um modelo padrão

routes: contém todas as rotas da aplicação separada por módulos (serviços). Cada arquivo será uma API executando em um endereço diferente.  
ex: userRoute -> contém todas as rotas que serão enviadas para fazer CRUD de usuários

services: implementação de serviços exteriores que serão utilizados no projeto, como serviço de email e Google Agenda

Ex: todas as requisições que serão enviadas para o serviço de usuários, será direcionado para o arquivo userRoute, O mesmo usará um arquivo que servirá de modelo de validação de dados dos usuários, o "userModel" dentro da pasta Models, e o serviço também deverá chamar dentro de suas rotas, um arquivo de controller chamado "Controller_user" dentro da pasta de Controllers, para realizar a lógica de negócio da entidade Usuário, arquivo este que chama a conexão com o banco de dados e realiza operações no banco, como operações básicas de CRUD.


