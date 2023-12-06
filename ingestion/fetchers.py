import aiohttp
import asyncio
import websockets
import json

async def fetch_from_rest_api(url, headers=None):
    """
    Asynchronously fetches data from a REST API.

    Args:
    url (str): The URL of the REST API.
    headers (dict, optional): Headers to include in the request.

    Returns:
    dict: The JSON response data.
    """
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            return await response.json()

async def fetch_from_websocket(uri):
    """
    Asynchronously fetches data from a WebSocket.

    Args:
    uri (str): The URI of the WebSocket.

    Returns:
    str: The data received from the WebSocket.
    """
    async with websockets.connect(uri) as ws:
        return await ws.recv()

async def fetch_data():
    sources_config = load_config('sources.json')

    for source in sources_config['sources']:
        if source['type'] == 'REST':
            headers = source.get('headers')
            data = await fetch_from_rest_api(source['endpoint'], headers)
            print(f"Data from {source['endpoint']}: {data}")
        elif source['type'] == 'WebSocket':
            data = await fetch_from_websocket(source['uri'])
            print(f"Data from {source['uri']}: {data}")
