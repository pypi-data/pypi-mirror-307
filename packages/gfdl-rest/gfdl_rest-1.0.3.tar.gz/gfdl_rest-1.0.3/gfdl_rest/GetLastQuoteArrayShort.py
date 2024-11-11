from .base_api import BaseAPI

class GetLastQuoteArrayShort(BaseAPI):
    def Get_LastQuoteArrayShort(self, exchange, instrument_identifiers,isShortIdentifiers=None):
        endpoint = "GetLastQuoteArrayShort/"
        params = {
            'exchange': exchange,
            'instrumentIdentifiers': instrument_identifiers
        }
        if isShortIdentifiers:
            params['isShortIdentifiers'] = isShortIdentifiers
        return self._get(endpoint, params)
