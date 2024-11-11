from .base_api import BaseAPI

class GetLimitation(BaseAPI):
    def Get_Limitation(self):
        endpoint = "GetLimitation/"
        

        return self._get(endpoint) 
