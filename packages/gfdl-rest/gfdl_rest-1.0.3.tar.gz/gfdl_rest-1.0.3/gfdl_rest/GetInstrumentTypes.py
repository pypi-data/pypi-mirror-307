from .base_api import BaseAPI

class GetInstrumentTypes(BaseAPI):
    def Get_InstrumentTypes(self,exchange):
        endpoint = "GetInstrumentTypes/"
        params = {
            'exchange': exchange
            
        }
        

        return self._get(endpoint,params)  
