import asyncio
import websockets
import threading

clients = set()

async def register_client(websocket):
    """ Register a new WebSocket client. """
    clients.add(websocket)

async def unregister_client(websocket):
    """ Unregister a WebSocket client. """
    clients.remove(websocket)

async def echo_server(websocket, path):
    """ Handle incoming WebSocket connections. """
    await register_client(websocket)
    try:
        await websocket.wait_closed()
    finally:
        await unregister_client(websocket)

def start_server():
    """ Start the WebSocket server. """
    return websockets.serve(echo_server, "localhost", 6790)

def input_loop(loop):
    """ Loop for inputting and sending messages. """
    while True:
        try:
            message = input("Enter message to send: ")
            asyncio.run_coroutine_threadsafe(broadcast(message), loop)
        except (EOFError, KeyboardInterrupt):
            print("Input loop terminated.")
            break

async def broadcast(message):
    """ Broadcast a message to all connected clients. """
    if clients:  # Check if there are any connected clients
        await asyncio.gather(*(client.send(message) for client in clients))

def main():
    loop = asyncio.get_event_loop()
    server = start_server()
    loop.run_until_complete(server)
    print("WebSocket server started on ws://localhost:6790")
    input_thread = threading.Thread(target=input_loop, args=(loop,))
    input_thread.start()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Server stopped by user.")
    finally:
        loop.close()
        input_thread.join()  # Ensure the input thread is also stopped

if __name__ == "__main__":
    main()
