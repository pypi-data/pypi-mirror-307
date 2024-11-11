from .base_api import BaseAPI

class GetLastQuoteOptionChain(BaseAPI):
    
    def Get_LastQuoteOptionChain(self, exchange, product, expiry=None, option_type=None, strike_price=None):
        endpoint = "GetLastQuoteOptionChain/"
        params = {
            'exchange': exchange,
            'product': product
        }
        if expiry:
            params['expiry'] = expiry
        if option_type:
            params['optionType'] = option_type
        if strike_price:
            params['strikePrice'] = strike_price
        return self._get(endpoint, params)
