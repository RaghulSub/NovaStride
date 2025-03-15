import streamlit as st
import json
import socket

# Socket server configuration (server runs on port 8000)
HOST = "localhost"
PORT = 8000

def send_json_data(data):
    """
    Sends JSON data over a socket to a server and collects multiple responses.
    The server sends each processed event as a JSON string terminated by a newline.
    Returns a list of JSON responses.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            # Convert the JSON data to a string then encode to bytes.
            json_data = json.dumps(data).encode("utf-8")
            client_socket.sendall(json_data)
            
            # Receive responses until the connection is closed.
            received_data = ""
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                received_data += chunk.decode("utf-8")
            
            # Split received data on newline to get each JSON response.
            responses = []
            for line in received_data.split("\n"):
                if line.strip():
                    responses.append(json.loads(line))
            return responses
    except Exception as e:
        st.error(f"Socket connection failed: {e}")
        return None

st.title("Upload JSON Log File and Send via Socket")
st.markdown("Upload your JSON log file (which should contain a JSON list of events) and click the button to send it to the socket server.")

# File uploader for the JSON file.
uploaded_file = st.file_uploader("Choose a JSON log file", type=["json"])

if uploaded_file is not None:
    try:
        # Parse the uploaded JSON file.
        data = json.load(uploaded_file)
        st.subheader("Uploaded JSON Data")
        st.json(data)
        
        # Button to send data via the socket.
        if st.button("Send JSON to Socket Server"):
            responses = send_json_data(data)
            if responses is not None:
                st.success("Data sent successfully!")
                st.subheader("Server Responses")
                # Display each JSON response from the server.
                for response in responses:
                    st.json(response)
            else:
                st.error("Failed to receive a response from the server.")
    except Exception as e:
        st.error(f"Error reading JSON file: {e}")
