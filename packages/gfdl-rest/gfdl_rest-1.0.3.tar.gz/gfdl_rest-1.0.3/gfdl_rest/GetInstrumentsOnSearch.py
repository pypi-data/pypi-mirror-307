 
from .base_api import BaseAPI

class GetInstrumentsOnSearch(BaseAPI):
    def Get_InstrumentsOnSearch(self, exchange, search,  instrument_type=None, option_type=None,expiry=None,StrikePrice=None, only_active=False,detailed_info=False):
        endpoint = "GetInstrumentsOnSearch/"
        params = {
            'exchange': exchange,
            'search': search
            
        }
        if instrument_type:
            params['instrumentType'] = instrument_type
        if option_type:
            params['optionType'] = option_type
        if expiry:
            params['expiry'] = expiry
        if StrikePrice:
            params['StrikePrice'] = StrikePrice
        if only_active:
            params['onlyActive'] = only_active
        if detailed_info:
            params['detailedInfo'] = detailed_info
        return self._get(endpoint, params)