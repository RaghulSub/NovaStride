import socket
import json
import threading
from Predict import process_data
import os
from dotenv import load_dotenv

load_dotenv()

HOST  = os.getenv("HOST",'0.0.0.0')
PORT = int(os.getenv("PORT",8000))




def start_server():
    """
    Starts a socket server that listens for incoming JSON data,
    processes it, and sends back a response.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Socket Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

def handle_client(conn, addr):
    """
    Handles communication with a single client.
    """
    with conn:
        print(f"Connected by {addr}")

        try:
            # Receive data
            data = conn.recv(4096).decode('utf-8')
            if not data:
                return

            json_data = json.loads(data)  # Parse JSON

            # Process data
            response_data = process_data(json_data)
            response_json = json.dumps(response_data)

            # Send back response
            conn.sendall(response_json.encode('utf-8'))

        except json.JSONDecodeError:
            error_msg = json.dumps({"error": "Invalid JSON format"})
            conn.sendall(error_msg.encode('utf-8'))

if __name__ == "__main__":
    start_server()
