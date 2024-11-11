from .base_api import BaseAPI

class GetServerInfo(BaseAPI):
    def Get_ServerInfo(self):
        endpoint = "GetServerInfo/"
        return self._get(endpoint) 
