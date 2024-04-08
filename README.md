# PI-StreetWise-ERP-3Semestre
Este é um projeto de um sistema de gerenciamento para estúdios de tatuagem feito com Python (FastAPI) e Javascript (React), utilizando banco de dados não-relacional, e arquitetura orientada a microsserviços
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
O projeto contém uma arquitetura orientada a serviços, que possui uma estrutura front-end em formato de SPA (Single Page Applications) localizada na pasta "front" (apenas de teste) que enviará requisições para os serviços no back-end.

Dentro da pasta routes, há os serviços com suas repectivas rotas, importante ressaltar que cada serviço será uma API rodando em um endereço diferente, ex: O serviço de usuários, como CRUD, e login, será o arquivo "userRoute" que se encontra dentro da pasta routes, sendo assim, todas as requisições que serão enviadas para o serviço de usuários, será direcionado para o arquivo userRoute, O mesmo usará um arquivo que servirá de modelo de validação de dados, o "userModel", dentro da pasta Models, e o serviço também deverá chamar dentro de suas rotas, um arquivo de controller chamado "Controller_user", dentro da pasta de Controllers, para realizar a lógica de negócio da entidade Usuário, como operações básicas de CRUD.

O projeto também contém uma pasta de configs, para configurações de possíveis subsistemas, como o banco de dados MongoDB, já implementado.

Há também uma pasta chamada "services" para implementação de outros módulos e APIS exteriores que serão consumidas na aplicação, como o serviço de email, que terá sua própria lógica de negócio
