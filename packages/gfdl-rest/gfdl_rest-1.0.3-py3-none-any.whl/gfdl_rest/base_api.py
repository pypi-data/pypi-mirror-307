import requests

class BaseAPI:
    def __init__(self, base_url, access_key, xml=False, format_csv=False):
        self.base_url = base_url
        self.access_key = access_key
        self.xml = xml
        self.format_csv = format_csv

    def _get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        if params is None:
            params = {}
        
        # Append mandatory parameters
        params['accessKey'] = self.access_key
        
        # Append conditional parameters
        if self.xml:
            params['xml'] = 'true'
        if self.format_csv:
            params['format'] = 'CSV'
        
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
        
        # Determine the content type and handle the response accordingly
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
           
            return response.json()
        elif 'application/xml' in content_type or 'text/xml' in content_type:
            
            return response.text
        elif 'text/csv' in content_type or 'application/csv' in content_type:
            
            return response.text
        else:
            return response.text