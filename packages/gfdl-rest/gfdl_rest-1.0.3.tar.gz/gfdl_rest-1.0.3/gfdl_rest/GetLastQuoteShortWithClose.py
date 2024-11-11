from .base_api import BaseAPI

class GetLastQuoteShortWithClose(BaseAPI):
    def Get_LastQuoteShortWithClose(self, exchange, instrument_identifier,isShortIdentifiers=None):
        endpoint = "GetLastQuoteShortWithClose/"
        params = {
            'exchange': exchange,
            'instrumentIdentifier': instrument_identifier
        }
        if isShortIdentifiers:
            params['isShortIdentifiers'] = isShortIdentifiers
        return self._get(endpoint, params) 
