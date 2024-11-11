from .base_api import BaseAPI

class GetExpiryDates(BaseAPI):
    def Get_ExpiryDates(self,exchange,product=None,instrumentType=None):
        endpoint = "GetExpiryDates/"
        params = {
            'exchange': exchange
            
        }
        if instrumentType is not None:
            params['instrumentType'] = instrumentType
        if product is not None:
            params['product'] = product
        

        return self._get(endpoint,params) 
