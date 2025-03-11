# API Interna TechFlow

Este repositório contém o código da API interna da TechFlow, uma empresa fictícia focada em gerenciamento de projetos e tarefas.

## Convenções e Padrões

A API da TechFlow segue um conjunto de convenções e padrões para garantir consistência e facilitar a manutenção.

### Nomenclatura

* **Snake Case:** Nomes de funções e variáveis utilizam o padrão `snake_case` (por exemplo, `create_project`, `user_id`).
* **Pascal Case:** Nomes de classes utilizam o padrão `PascalCase` (por exemplo, `ProjectDAO`, `UserNotFoundError`).

### Formato de Resposta da API

As respostas da API seguem um formato JSON padronizado:

```json
{
  "status": "success" | "error",
  "data": {}, // Dados da resposta (se status for "success")
  "message": "Mensagem de erro" // Mensagem de erro (se status for "error")
}
```

### Tratamento de Erros
A API utiliza exceções personalizadas para tratamento de erros (por exemplo, ProjectNotFoundError, UnauthorizedError).
As respostas de erro incluem mensagens detalhadas para facilitar o diagnóstico.
Os status HTTP são usados para indicar o tipo de erro (por exemplo, 404 para "Não encontrado", 400 para "Requisição inválida").

### Autenticação
A API utiliza autenticação baseada em tokens JWT (JSON Web Tokens).
Os tokens são enviados no cabeçalho Authorization no formato Bearer <token>.
Os tokens expiram após 1 hora.

### Acesso a Dados
A API utiliza um banco de dados relacional simulado para persistência de dados.
O padrão DAO (Data Access Object) é utilizado para abstrair o acesso ao banco de dados e separar a lógica de acesso a dados da lógica de negócios.

### Simulação de Banco de dados
O Banco de dados é simulado em memória, utilizando dicionários e listas.
Isso serve apenas para exemplo, em um ambiente real, um banco de dados relacional como PostgreSQL ou MySQL seria usado.

### Exemplo de Uso
Para testar a API, você pode simular requisições HTTP utilizando ferramentas como curl ou Postman, ou executar o script python presente no arquivo.

#### Exemplo de requisição (curl):

##### bash
```bash
curl -X POST -H "Authorization: Bearer <seu_token>" -H "Content-Type: application/json" -d '{"name": "Novo Projeto", "description": "Descrição do projeto"}' http://<seu_servidor>/projects
Exemplo de requisição (python):
```

##### Python

```python
#Simulando usuario para teste.
UserDAO.create_user({"name":"test user"})
token = generate_jwt(1)

#Simulando uma requisição de criação de projeto.
request_create_project = Request({"Authorization": f"Bearer {token}"}, '{"name": "New Project", "description": "Project description"}')
print(create_project(request_create_project))
```

### Exceções
ProjectNotFoundError: Lançada quando um projeto não é encontrado.
TaskNotFoundError: Lançada quando uma tarefa não é encontrada.
UserNotFoundError: Lançada quando um usuário não é encontrado.
UnauthorizedError: Lançada quando a autenticação falha.

### Configuração
SECRET_KEY: Chave secreta para geração e validação de tokens JWT.
DATABASE: Simulação do banco de dados.