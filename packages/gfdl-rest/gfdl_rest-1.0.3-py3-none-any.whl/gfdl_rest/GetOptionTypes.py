from .base_api import BaseAPI

class GetOptionTypes(BaseAPI):
    def Get_OptionTypes(self,exchange,instrumentType=None,product=None,expiry=None):
        endpoint = "GetOptionTypes/"
        params = {
            'exchange': exchange
            
        }
        if instrumentType is not None:
            params['instrumentType'] = instrumentType
        if product is not None:
            params['product'] = product
        if expiry is not None:
            params['expiry'] = expiry
        

        return self._get(endpoint,params) 
