from .fetchers import fetch_from_rest_api, fetch_from_websocket

class RestApiAdapter:
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers

    async def fetch_data(self):
        """ Fetch data using the REST API fetcher. """
        return await fetch_from_rest_api(self.url, self.headers)

class WebSocketAdapter:
    def __init__(self, uri):
        self.uri = uri

    async def fetch_data(self):
        """ Fetch data using the WebSocket fetcher. """
        return await fetch_from_websocket(self.uri)
