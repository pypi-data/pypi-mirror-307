from .base_api import BaseAPI

class GetHistoryGreeks(BaseAPI):
    def GetHistory_Greeks(self, exchange, instrument_identifier, isShortIdentifier=None, max_results=None,from_timestamp=None, to_timestamp=None):
        endpoint = "GetHistory/"
        params = {
            'exchange': exchange,
            'instrumentIdentifier': instrument_identifier,
        }
        if isShortIdentifier:
            params['isShortIdentifier'] = isShortIdentifier
        if max_results:
            params['max'] = max_results
        if from_timestamp:
            params['from'] = from_timestamp
        if to_timestamp:
            params['to'] = to_timestamp
        return self._get(endpoint, params)
