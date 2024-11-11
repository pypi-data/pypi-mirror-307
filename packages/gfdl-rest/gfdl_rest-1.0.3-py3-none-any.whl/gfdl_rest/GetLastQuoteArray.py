from .base_api import BaseAPI

class GetLastQuoteArray(BaseAPI):
    def GetLastQuoteArray(self, exchange, instrument_identifiers,isShortIdentifiers=None):
        endpoint = "GetLastQuoteArray/"
        params = {
            'exchange': exchange,
            'instrumentIdentifiers': instrument_identifiers
        }
        if isShortIdentifiers:
            params['isShortIdentifiers'] = isShortIdentifiers
        return self._get(endpoint, params)
