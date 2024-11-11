from .base_api import BaseAPI

class GetTopGainersLosers(BaseAPI):
    def Get_TopGainersLosers(self, exchange, count):
        endpoint = "GetTopGainersLosers/"
        params = {
            'exchange': exchange,
            'count': count
        }
        
        return self._get(endpoint, params) 