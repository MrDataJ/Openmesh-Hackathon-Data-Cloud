import asyncio
import websockets
import json

class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = set()

    async def register(self, websocket):
        """ Register a WebSocket connection for broadcasting. """
        self.clients.add(websocket)

    async def unregister(self, websocket):
        """ Unregister a WebSocket connection. """
        self.clients.remove(websocket)

    async def broadcast(self, message):
        """ Broadcast a message to all connected clients. """
        if self.clients:
            # Create a list of tasks for sending messages
            tasks = [asyncio.create_task(client.send(message)) for client in self.clients]
            # Wait for all tasks to complete
            await asyncio.gather(*tasks)

    async def serve(self, websocket, path):
        """ Handle incoming WebSocket connections. """
        await self.register(websocket)
        try:
            await websocket.wait_closed()
        finally:
            await self.unregister(websocket)

    def start_server(self):
        """ Start the WebSocket server. """
        return websockets.serve(self.serve, self.host, self.port)

# Example usage
if __name__ == "__main__":
    server = WebSocketServer('localhost', 6789)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.start_server())
    print(f"WebSocket Server started on ws://{server.host}:{server.port}")
    loop.run_forever()
