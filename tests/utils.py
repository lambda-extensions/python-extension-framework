import json

class FakeResponse:
    def __init__(self, response, headers=None):
        self._response = response
        self.headers = headers
        self.text = response

    def read(self):
        return self._response

    def json(self):
        return json.loads(self._response)

