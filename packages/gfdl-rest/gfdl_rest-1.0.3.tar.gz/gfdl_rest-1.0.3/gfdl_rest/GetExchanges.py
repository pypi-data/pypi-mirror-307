from .base_api import BaseAPI

class GetExchanges(BaseAPI):
    def Get_Exchanges(self):
        endpoint = "GetExchanges/"
        return self._get(endpoint) 
