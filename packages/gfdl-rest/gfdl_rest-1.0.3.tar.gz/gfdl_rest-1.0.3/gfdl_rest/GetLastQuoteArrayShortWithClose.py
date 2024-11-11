from .base_api import BaseAPI

class GetLastQuoteArrayShortWithClose(BaseAPI):
    def Get_LastQuoteArrayShortWithClose(self, exchange, instrument_identifiers,isShortIdentifiers=None):
        endpoint = "GetLastQuoteArrayShortWithClose/"
        params = {
            'exchange': exchange,
            'instrumentIdentifiers': instrument_identifiers
        }
        if isShortIdentifiers:
            params['isShortIdentifiers'] = isShortIdentifiers
        return self._get(endpoint, params)