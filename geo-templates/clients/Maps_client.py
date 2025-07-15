import googlemaps
from datetime import datetime
from core.error_handler import APICredentialsError, APIRequestError
from core.logging_config import get_logger

# Pega uma instância do logger padronizado
logger = get_logger(__name__)

class GoogleMapsClient:
    """
    Cliente padronizado para interagir com as APIs do Google Maps.
    Implementa retentativas (retries), logging estruturado e tratamento de erro.
    """
    def __init__(self, api_key: str):
        if not api_key:
            logger.error("API Key do Google Maps não foi fornecida.")
            raise APICredentialsError("API Key é obrigatória.")
        
        self.gmaps = googlemaps.Client(key=api_key)
        logger.info("Cliente do Google Maps inicializado com sucesso.")

    def get_directions(self, origin: tuple, destination: tuple, mode: str = "driving") -> dict:
        """
        Busca direções entre uma origem e um destino.
        
        Args:
            origin (tuple): Tupla de (latitude, longitude) da origem.
            destination (tuple): Tupla de (latitude, longitude) do destino.
            mode (str): Modo de transporte (driving, walking, bicycling, transit).
            
        Returns:
            dict: O primeiro resultado da rota encontrado pela API.
            
        Raises:
            APIRequestError: Se a API do Google Maps retornar um erro ou nenhuma rota.
        """
        try:
            logger.debug(f"Buscando rotas de {origin} para {destination} via {mode}.")
            directions_result = self.gmaps.directions(origin,
                                                      destination,
                                                      mode=mode,
                                                      departure_time=datetime.now())
            
            if not directions_result:
                logger.warning("Nenhuma rota encontrada para os pontos fornecidos.")
                raise APIRequestError("Nenhuma rota encontrada.")

            # Retorna a primeira rota, que é o padrão da nossa implementação
            return directions_result[0]

        except googlemaps.exceptions.ApiError as e:
            logger.error(f"Erro na API do Google Maps: {e}")
            raise APIRequestError(f"Erro ao chamar a API do Google Maps: {e}") from e