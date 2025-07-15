class GeoAPIError(Exception):
    """Base para exceções da nossa API."""
    pass

class APICredentialsError(GeoAPIError):
    """Erro para credenciais de API inválidas ou ausentes."""
    pass

class APIRequestError(GeoAPIError):
    """Erro durante uma requisição a uma API externa."""
    pass