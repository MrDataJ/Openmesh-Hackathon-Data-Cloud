import asyncio
import websockets
import json

class WebSocketServer:
    def __init__(self, host, port, peers):
        self.host = host
        self.port = port
        self.clients = set()
        self.peers = peers  # List of other WebSocket server URIs to connect to

    async def register(self, websocket):
        """ Register a WebSocket connection for broadcasting. """
        self.clients.add(websocket)

    async def unregister(self, websocket):
        """ Unregister a WebSocket connection. """
        self.clients.remove(websocket)

    async def broadcast(self, message):
        """ Broadcast a message to all connected clients. """
        if self.clients:
            tasks = [asyncio.create_task(client.send(message)) for client in self.clients]
            await asyncio.gather(*tasks)

    async def serve(self, websocket, path):
        """ Handle incoming WebSocket connections. """
        await self.register(websocket)
        try:
            await websocket.wait_closed()
        finally:
            await self.unregister(websocket)

    async def connect_to_peers(self):
        """ Connect to other WebSocket servers (peers) and relay messages. """
        for uri in self.peers:
            try:
                async with websockets.connect(uri) as websocket:
                    # Here, you could implement logic to send or relay messages to this peer
                    pass
            except Exception as e:
                print(f"Error connecting to {uri}: {e}")

    def start_server(self):
        """ Start the WebSocket server. """
        return websockets.serve(self.serve, self.host, self.port)

# Example usage
if __name__ == "__main__":
    peers = ["ws://othernode1.example.com:6789", "ws://othernode2.example.com:6789"]  # Example peers
    server = WebSocketServer('localhost', 6789, peers)
    loop = asyncio.get_event_loop()

    # Start server and connect to peers
    loop.run_until_complete(server.start_server())
    loop.create_task(server.connect_to_peers())

    print(f"WebSocket Server started on ws://{server.host}:{server.port}")
    loop.run_forever()
