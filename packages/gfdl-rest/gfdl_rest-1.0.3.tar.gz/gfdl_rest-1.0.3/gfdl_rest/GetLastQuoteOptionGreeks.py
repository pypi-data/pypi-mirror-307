from .base_api import BaseAPI

class GetLastQuoteOptionGreeks(BaseAPI):
    def Get_LastQuoteOptionGreeks(self,exchange,tokens,detailedInfo=None):
        endpoint = "GetLastQuoteOptionGreeks/"
        params = {
            'exchange': exchange,
            'tokens':tokens
            
        }
        if detailedInfo is not None:
            params['detailedInfo'] = detailedInfo
        

        return self._get(endpoint,params) 
 

