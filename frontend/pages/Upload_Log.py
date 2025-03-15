import streamlit as st
import asyncio
import websockets
import json

async def send_json_data(json_data):
    uri = "ws://localhost:8000/ws"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps(json_data))
            responses = []
            
            while True:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5)  # Timeout if no response in 5 sec
                    responses.append(json.loads(response))
                except asyncio.TimeoutError:
                    break  # Stop if no data received for 5 seconds
                except websockets.exceptions.ConnectionClosed:
                    break  # Stop if server closes connection
            
            return responses
    except Exception as e:
        return [{"error": f"WebSocket error: {e}"}]

st.title("WebSocket JSON Sender")

uploaded_file = st.file_uploader("Upload JSON File", type=["json"])

if uploaded_file is not None:
    json_data = json.load(uploaded_file)
    st.json(json_data)

    if st.button("Send JSON via WebSocket"):
        responses = asyncio.run(send_json_data(json_data))
        st.subheader("Server Responses")
        for response in responses:
            st.json(response)
