import streamlit as st
import pandas as pd
import plotly.express as px
import socket
import json
import threading
import time

# Function to receive data from the socket
def receive_data(sock, data_list):
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            if data:
                data_json = json.loads(data)
                data_list.append(data_json)
        except Exception as e:
            st.error(f"Error receiving data: {e}")
            break

# Connect to the socket server
def init_socket_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('0.0.0.0', 8000))
    return sock

# Initialize socket connection
sock = init_socket_connection()

# Shared list to store incoming data
data_list = []

# Start a background thread to receive data
threading.Thread(target=receive_data, args=(sock, data_list), daemon=True).start()

# Streamlit dashboard layout
st.title("Real-Time System Monitoring Dashboard")

# Initialize empty plots
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

# Main loop to update the dashboard
while True:
    if data_list:
        # Convert list to DataFrame
        df = pd.DataFrame(data_list)
        # Convert 'time' to datetime
        df['time'] = pd.to_datetime(df['time'])
        # Sort by time
        df = df.sort_values(by='time')
        # Update plots
        update_plots(df)
        # Limit the data list to the last 100 entries to prevent memory issues
        data_list = data_list[-100:]
    # Refresh every second
    time.sleep(1)
