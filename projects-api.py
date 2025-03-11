import json
import jwt
from datetime import datetime, timedelta

# Configurações fictícias
SECRET_KEY = "techflow_secret"
DATABASE = {"projects": [], "tasks": [], "users": []}  # Simulação de banco de dados

# Exceções personalizadas
class ProjectNotFoundError(Exception):
    pass

class TaskNotFoundError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

# DAO (Data Access Object) simulado
class ProjectDAO:
    @staticmethod
    def get_project_by_id(project_id):
        for project in DATABASE["projects"]:
            if project["id"] == project_id:
                return project
        raise ProjectNotFoundError(f"Project with ID {project_id} not found.")

    @staticmethod
    def create_project(project_data):
        project_id = len(DATABASE["projects"]) + 1
        project_data["id"] = project_id
        DATABASE["projects"].append(project_data)
        return project_data

class TaskDAO:
    @staticmethod
    def get_task_by_id(task_id):
        for task in DATABASE["tasks"]:
            if task["id"] == task_id:
                return task
        raise TaskNotFoundError(f"Task with ID {task_id} not found.")

    @staticmethod
    def create_task(task_data):
        task_id = len(DATABASE["tasks"]) + 1
        task_data["id"] = task_id
        DATABASE["tasks"].append(task_data)
        return task_data

class UserDAO:
    @staticmethod
    def get_user_by_id(user_id):
        for user in DATABASE["users"]:
            if user["id"] == user_id:
                return user
        raise UserNotFoundError(f"User with ID {user_id} not found.")

    @staticmethod
    def create_user(user_data):
        user_id = len(DATABASE["users"]) + 1
        user_data["id"] = user_id
        DATABASE["users"].append(user_data)
        return user_data

# Funções de autenticação
def generate_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError("Token expired.")
    except jwt.InvalidTokenError:
        raise UnauthorizedError("Invalid token.")

# Funções da API
def create_project(request):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise UnauthorizedError("Missing or invalid authorization header.")
        token = auth_header.split("Bearer ")[1]
        user_id = decode_jwt(token)

        project_data = json.loads(request.body)
        project_data["created_by"] = user_id
        new_project = ProjectDAO.create_project(project_data)
        return json.dumps({"status": "success", "data": new_project})
    except (UnauthorizedError, ValueError, KeyError) as e:
        return json.dumps({"status": "error", "message": str(e)}), 400

def get_project(request, project_id):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise UnauthorizedError("Missing or invalid authorization header.")
        token = auth_header.split("Bearer ")[1]
        decode_jwt(token)

        project = ProjectDAO.get_project_by_id(project_id)
        return json.dumps({"status": "success", "data": project})
    except (ProjectNotFoundError, UnauthorizedError) as e:
        return json.dumps({"status": "error", "message": str(e)}), 404

# Exemplo de uso (simulação de requisições)
class Request:
    def __init__(self, headers, body):
        self.headers = headers
        self.body = body

#Simulando usuario para teste.
UserDAO.create_user({"name":"test user"})
token = generate_jwt(1)

#Simulando uma requisição de criação de projeto.
request_create_project = Request({"Authorization": f"Bearer {token}"}, '{"name": "New Project", "description": "Project description"}')
print(create_project(request_create_project))

#Simulando uma requisição de busca de projeto.
request_get_project = Request({"Authorization": f"Bearer {token}"}, '{}')
print(get_project(request_get_project, 1))