#!/usr/bin/env python
# coding: utf-8

#  **Server Side**

# In[1]:


# import the necessary libraries

import asyncio
import websockets
from datetime import datetime


# In[ ]:


# keep connected clients and their names
connected_clients = {}

async def handle_message(websocket, path):
    try:
        # Expecting the first message to be the client's name
        name = await websocket.recv()
        connected_clients[websocket] = name
        print(f"New client '{name}' connected. Total clients: {len(connected_clients)}")

        async for message in websocket:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # check if the message is a private message or it should be sent to all clients
            if message.startswith("DM") or message.startswith("dm"):
                _, recipient_name, private_msg = message.split(" ", 2)
                for client, client_name in connected_clients.items():
                    if client_name == recipient_name:
                        await client.send(f"Private message from {name} at {timestamp}: {private_msg}")
                        break
            else:
                # broadcast the message to all clients except the sender
                sender_name = connected_clients[websocket]
                formatted_message = f"{timestamp} - {sender_name}: {message}"
                
                for client, client_name in connected_clients.items():
                    if client != websocket:
                        await client.send(formatted_message)
                print(formatted_message)

    except websockets.ConnectionClosedError:
        if websocket in connected_clients:
            name = connected_clients.pop(websocket)
            print(f"Client '{name}' disconnected. Total clients: {len(connected_clients)}")

# start the WebSocket server
start_server = websockets.serve(handle_message, "localhost", 8765, ping_interval=None, ping_timeout=None)

# run the server
print("Server connection is started...")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

