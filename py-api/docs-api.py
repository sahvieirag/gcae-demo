import json
import uuid
from datetime import datetime

# Simulação de banco de dados para documentos
DOCUMENT_DATABASE = {}

# Funções da API para gerenciamento de documentos
def create_document(request):
    try:
        data = json.loads(request.body)
        document_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        document = {
            "id": document_id,
            "title": data["title"],
            "content": data["content"],
            "created_at": timestamp,
            "updated_at": timestamp,
        }
        DOCUMENT_DATABASE[document_id] = document
        return json.dumps({"status": "success", "data": document}), 201
    except (ValueError, KeyError) as e:
        return json.dumps({"status": "error", "message": str(e)}), 400

def get_document(document_id):
    try:
        if document_id not in DOCUMENT_DATABASE:
            return json.dumps({"status": "error", "message": "Document not found"}), 404
        document = DOCUMENT_DATABASE[document_id]
        return json.dumps({"status": "success", "data": document}), 200
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)}), 500

def update_document(request, document_id):
    try:
        if document_id not in DOCUMENT_DATABASE:
            return json.dumps({"status": "error", "message": "Document not found"}), 404
        data = json.loads(request.body)
        document = DOCUMENT_DATABASE[document_id]
        document["title"] = data.get("title", document["title"])
        document["content"] = data.get("content", document["content"])
        document["updated_at"] = datetime.now().isoformat()
        DOCUMENT_DATABASE[document_id] = document
        return json.dumps({"status": "success", "data": document}), 200
    except (ValueError, KeyError) as e:
        return json.dumps({"status": "error", "message": str(e)}), 400

# Exemplo de uso (simulação de requisições)
class Request:
    def __init__(self, body):
        self.body = body

# Simulando requisições
request_create_document = Request('{"title": "Manual de Integração", "content": "Conteúdo do manual"}')
response_create, status_create = create_document(request_create_document)
print(response_create)

document_id = json.loads(response_create)[ "data"]["id"]

response_get, status_get = get_document(document_id)
print(response_get)

request_update_document = Request('{"title": "Manual de Integração Atualizado"}')
response_update, status_update = update_document(request_update_document, document_id)
print(response_update)