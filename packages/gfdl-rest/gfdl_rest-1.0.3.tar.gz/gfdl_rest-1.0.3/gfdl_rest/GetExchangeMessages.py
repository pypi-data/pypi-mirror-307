from .base_api import BaseAPI

class GetExchangeMessages(BaseAPI):
    def Get_Exchange_Messages(self,exchange):
        endpoint = "GetExchangeMessages/"
        params = {
            'exchange': exchange
        }
        

        return self._get(endpoint,params) 