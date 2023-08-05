#!/usr/bin/env python
# coding: utf-8

#  **Client Side**

# In[1]:


# importing the necessary libraries

import asyncio
import websockets
import aioconsole


# In[ ]:


async def handle_message(websocket):
    try:
        async for message in websocket:
            print(f"{message}")

    except websockets.ConnectionClosedError:
        print("Connection to the server is closed.")

async def send_message(websocket, name):
    while True:
        message = await aioconsole.ainput(" ")
        await websocket.send(f"{message}")

async def main():
    name = input("Enter your name: ")
    async with websockets.connect("ws://localhost:8765") as websocket:
        # send the client name as the first message
        await websocket.send(name)
        print("Successfully connected to the server.")
        try:
            await asyncio.gather(handle_message(websocket), send_message(websocket, name))
        except websockets.ConnectionClosedError:
            print("Connection to the server is closed.")
            
# run the server
asyncio.get_event_loop().run_until_complete(main())

