from .base_api import BaseAPI

class GetLastQuoteOptionGreeksChain(BaseAPI):
    
    def Get_LastQuoteOptionGreeksChain(self, exchange, product, expiry=None, option_type=None, strike_price=None):
        endpoint = "GetLastQuoteOptionGreeksChain/"
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
