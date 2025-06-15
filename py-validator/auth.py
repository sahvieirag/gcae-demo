from functools import wraps

def require_permission(permission: str):
    """
    Decorator para simular a verificação de permissão de um usuário.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"DEBUG: Verificando se o usuário tem a permissão '{permission}'...")
            # Lógica de verificação (aqui simplificada)
            # if not user_has_permission(permission):
            #     raise HTTPException(status_code=403, detail="Permissão negada.")
            return func(*args, **kwargs)
        return wrapper
    return decorator