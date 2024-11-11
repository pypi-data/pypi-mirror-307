from .base_api import BaseAPI

class GetProducts(BaseAPI):
    def Get_Products(self,exchange,instrumentType=None):
        endpoint = "GetProducts/"
        params = {
            'exchange': exchange
            
        }
        if instrumentType is not None:
            params['instrumentType'] = instrumentType
        
        

        return self._get(endpoint,params) 
