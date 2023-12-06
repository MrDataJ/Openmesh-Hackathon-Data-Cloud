import asyncio
import logging
from ingestion.adapters import RestApiAdapter, WebSocketAdapter
from processing.processor import process_data
from database.db_manager import DBManager
from websocket.server import WebSocketServer
from config.config import load_config
import json

logging.basicConfig(level=logging.INFO)

async def handle_rest_api(adapter, data_queue, polling_interval):
    while True:
        try:
            raw_data = await adapter.fetch_data()
            processed_data = process_data(raw_data)
            await data_queue.put(processed_data)
            await asyncio.sleep(polling_interval)
        except Exception as e:
            logging.error(f"Error in REST API ingestion: {e}")
            await asyncio.sleep(5)

async def handle_websocket(adapter, data_queue):
    while True:
        try:
            message = await adapter.fetch_data()
            processed_data = process_data(message)
            await data_queue.put(processed_data)
        except Exception as e:
            logging.error(f"Error in WebSocket ingestion: {e}")
            # Break or continue based on desired error handling
            break

async def broadcast_data(websocket_server, data_queue, db_manager):
    while True:
        data = await data_queue.get()
        if not isinstance(data, str):
            data = json.dumps(data)
        await websocket_server.broadcast(data)
        # Optionally, insert data into the database
        # db_manager.insert_data(...)

async def ingest_and_process_data(websocket_server, data_queue):
    connectors_config = load_config('connectors.json')['connectors']
    tasks = []
    for connector in connectors_config:
        if connector['type'] == 'REST':
            adapter = RestApiAdapter(connector['endpoint'], connector.get('headers'))
            task = asyncio.create_task(handle_rest_api(adapter, data_queue, connector['polling_interval']))
            tasks.append(task)
        elif connector['type'] == 'WebSocket':
            adapter = WebSocketAdapter(connector['uri'])
            task = asyncio.create_task(handle_websocket(adapter, data_queue))
            tasks.append(task)
    await asyncio.gather(*tasks)

async def main():
    logging.info("Starting the application...")
    db_manager = DBManager("database.sqlite")
    db_manager.create_connection()
    websocket_server = WebSocketServer('localhost', 6789)
    start_server = websocket_server.start_server()
    data_queue = asyncio.Queue()

    try:
        await asyncio.gather(
            start_server,
            ingest_and_process_data(websocket_server, data_queue),
            broadcast_data(websocket_server, data_queue, db_manager)
        )
    finally:
        db_manager.close_connection()

if __name__ == "__main__":
    asyncio.run(main())
