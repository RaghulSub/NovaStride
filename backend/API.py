import socket
import json
import threading
import os
from datetime import datetime
from dotenv import load_dotenv
from Predict import process_data  # Assuming Predict.py has process_data function

load_dotenv()

HOST = os.getenv("HOST", '0.0.0.0')
PORT = int(os.getenv("PORT", 8000))


def start_server():
    """
    Starts a socket server that listens for incoming JSON data,
    processes it, and sends back a response for each JSON entry.
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
            recieved_data = ""
            while True:
                chunk = conn.recv(4096).decode('utf-8')
                if not chunk:
                    break
                received_data +=  chunk
            if not received_data.strip():
                return 
            
            try:
                json_data = json.loads(received_data);
                if not isinstance(json_data,list):
                    print("Expected a JSON List")
                    raise ValueError("Expected a JSON List")
            except (json.JSONDecodeError, ValueError) as e:
                error_msg = json.dumps({"error":f"Invalid JSON format: {str(e)}"})
                conn.sendall((error_msg + "\n").encode('utf-8'))
                return 
            

        # try:
        #     # Receive data
        #     data = conn.recv(4096).decode('utf-8')
        #     if not data:
        #         return
        #     print(f"Received data: {data}")
        #     json_data = json.loads(data)  # Parse JSON list

            # Sort JSON list by eventTime
            sorted_json = sorted(json_data, key=lambda x: datetime.strptime(x["eventTime"], "%Y-%m-%dT%H:%M:%S.%fZ"))
            
            # Process and send each event separately
            for event in sorted_json:
                # response_data = process_data(event)  # Process one JSON at a time
                response_json = json.dumps(event)

                # Send processed data back to frontend immediately
                conn.sendall((response_json + "\n").encode('utf-8'))  # Send each JSON separately

        except json.JSONDecodeError:
            print("herre")
            error_msg = json.dumps({"Server error": "Invalid JSON format"})
            conn.sendall((error_msg + "\n").encode('utf-8'))
        
        except Exception as e:
            error_msg = json.dumps({"Server error": str(e)})
            conn.sendall((error_msg + "\n").encode('utf-8'))
        


if __name__ == "__main__":
    start_server()
