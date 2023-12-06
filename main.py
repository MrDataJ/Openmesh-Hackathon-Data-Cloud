import asyncio
import logging
from ingestion.adapters import RestApiAdapter, WebSocketAdapter
from processing.processor import process_data
from database.db_manager import DBManager
from websocket_server.server import WebSocketServer
from config.config import load_config  # Assuming you have a config_loader module
import json

logging.basicConfig(level=logging.INFO)

async def ingest_and_process_data(websocket_server):
    while True:  # Keep this coroutine running
        try:# Load source configurations
            connectors_config = load_config('connectors.json')['connectors']

            for connector in connectors_config:
                adapter = None
                if connector['type'] == 'REST':
                    adapter = RestApiAdapter(connector['endpoint'], connector.get('headers'))
                elif connector['type'] == 'WebSocket':
                    adapter = WebSocketAdapter(connector['uri'])

                if adapter:
                    print(f"Fetching data from {connector['type']} connector: {connector['name']}")
                    raw_data = await adapter.fetch_data()
                    processed_data = process_data(raw_data)
                    print(f"Processed data: {processed_data}")
                    # Serialize data if it's not a string
                    if not isinstance(processed_data, str):
                        processed_data = json.dumps(processed_data)
                    # Here you can save processed data to the database (optional)
                    # db_manager.insert_data(...)

                    # Broadcasting processed data to WebSocket clients
                    await websocket_server.broadcast(processed_data)
            await asyncio.sleep(5) # Wait for 5 seconds before fetching data again 
        except Exception as e:
            logging.error(f"Error in data ingestion: {e}")
            await asyncio.sleep(5)  # Wait a bit before retrying

async def main():
    logging.info("Starting the application...")

    # Initialize and set up database connection
    db_manager = DBManager("database.sqlite")
    db_manager.create_connection()

    # Set up and start the WebSocket server
    websocket_server = WebSocketServer('localhost', 6789)
    start_server = websocket_server.start_server()

    try:
        await asyncio.gather(
            start_server,
            ingest_and_process_data(websocket_server)
        )
    finally:
        # Ensure database connection is closed properly
        db_manager.close_connection()

if __name__ == "__main__":
    asyncio.run(main())
