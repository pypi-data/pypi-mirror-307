from .base_api import BaseAPI

class GetExchangeSnapshot(BaseAPI):
    def Get_ExchangeSnapshot(self, exchange,  periodicity, period, instrumentType=None,nonTraded=None, from_timestamp=None, to_timestamp=None):
        endpoint = "GetExchangeSnapshot/"
        params = {
            'exchange': exchange,
            
            'periodicity': periodicity,
            'period': period
        }
        if nonTraded:
            params['max'] = nonTraded
        if from_timestamp:
            params['from'] = from_timestamp
        if to_timestamp:
            params['to'] = to_timestamp
        if instrumentType:
            params['instrumentType'] = instrumentType
        return self._get(endpoint, params)
