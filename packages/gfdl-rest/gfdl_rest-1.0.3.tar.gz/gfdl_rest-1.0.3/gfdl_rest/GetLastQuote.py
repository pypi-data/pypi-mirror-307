from .base_api import BaseAPI

class GetLastQuote(BaseAPI):
    def Get_LastQuote(self, exchange, instrument_identifier,isShortIdentifiers):
        endpoint = "GetLastQuote/"
        params = {
            'exchange': exchange,
            'instrumentIdentifier': instrument_identifier
        }
        if isShortIdentifiers:
            params['isShortIdentifier'] = isShortIdentifiers
        return self._get(endpoint, params)