import streamlit as st
import asyncio
import websockets
import json
import pandas as pd
import plotly.express as px

# Define placeholders for plots
cpu_plot = st.empty()
memory_plot = st.empty()
disk_plot = st.empty()
bytes_plot = st.empty()

# Function to update plots
def update_plots(df):
    with cpu_plot:
        fig = px.line(df, x='time', y='cpuUtilization', title='CPU Utilization Over Time')
        st.plotly_chart(fig)
    with memory_plot:
        fig = px.line(df, x='time', y='memoryUsage', title='Memory Usage Over Time')
        st.plotly_chart(fig)
    with disk_plot:
        fig = px.line(df, x='time', y='diskUsage', title='Disk Usage Over Time')
        st.plotly_chart(fig)
    with bytes_plot:
        fig = px.line(df, x='time', y='bytesTransferred', title='Bytes Transferred Over Time')
        st.plotly_chart(fig)

def update_values(json_data):
    # Clear everything before updating
    st.session_state.clear()

    # Reinitialize the empty containers for plots
    global cpu_plot, memory_plot, disk_plot, bytes_plot
    cpu_plot = st.empty()
    memory_plot = st.empty()
    disk_plot = st.empty()
    bytes_plot = st.empty()

    df = pd.DataFrame(json_data)
    df['time'] = pd.to_datetime(df['time'])  # Convert 'time' to datetime
    df = df.sort_values(by='time')  # Sort by time
    update_plots(df)

async def send_json_data(json_data):
    uri = "ws://localhost:8000/ws"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps(json_data))
            responses = []
            
            while True:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5)
                    responses.append(json.loads(response))
                except asyncio.TimeoutError:
                    break
                except websockets.exceptions.ConnectionClosed:
                    break
            
            return responses
    except Exception as e:
        return [{"error": f"WebSocket error: {e}"}]

st.title("Cloud Service Provide Log Analyzer")

uploaded_file = st.file_uploader("Upload JSON File", type=["json"])

if uploaded_file is not None:
    json_data = json.load(uploaded_file)

    if st.button("Send JSON via WebSocket"):
        responses = asyncio.run(send_json_data(json_data))
        st.subheader("Server Responses")
        json_list = []
        for res in responses:
            input_json = {
                "time": res["eventTime"],
                "cpuUtilization": res["systemEvent"]["cpuUtilization"],
                "memoryUsage": res["systemEvent"]["memoryUsage"],
                "diskUsage": res["systemEvent"]["diskUsage"],
                "bytesTransferred": res["networkEvent"]["bytesTransferred"]
            }
            json_list.append(input_json)
        update_values(json_list)
