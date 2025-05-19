"""Minimal stub of the requests library for testing without external dependency."""

class Response:
    def __init__(self, json_data=None, status_code=200):
        self._json_data = json_data or {}
        self.status_code = status_code
    
    def json(self):
        return self._json_data

    def raise_for_status(self):
        pass

def get(url, headers=None, params=None):
    return Response()
