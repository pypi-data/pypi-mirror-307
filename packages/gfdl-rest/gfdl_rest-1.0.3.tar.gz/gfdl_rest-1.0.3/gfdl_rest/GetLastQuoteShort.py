from .base_api import BaseAPI

class GetLastQuoteShort(BaseAPI):
    def Get_LastQuoteShort(self, exchange, instrument_identifier,isShortIdentifiers=None):
        endpoint = "GetLastQuoteShort/"
        params = {
            'exchange': exchange,
            'instrumentIdentifier': instrument_identifier
        }
        if isShortIdentifiers:
            params['isShortIdentifiers'] = isShortIdentifiers
        return self._get(endpoint, params)
