from fastapi import FastAPI, WebSocket
import json
from datetime import datetime

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection established")

    try:
        while True:
            data = await websocket.receive_text()
            try:
                # Parse received data
                json_data = json.loads(data)

                # Validate JSON format
                if not isinstance(json_data, list):
                    await websocket.send_text(json.dumps({"error": "Expected a JSON list"}))
                    continue

                # Sort JSON list by eventTime
                sorted_json = sorted(json_data, key=lambda x: datetime.strptime(x["eventTime"], "%Y-%m-%dT%H:%M:%S.%fZ"))

                # Send sorted events back to client
                for event in sorted_json:
                    response_json = json.dumps(event)
                    print(event)
                    print("\n")
                    await websocket.send_text(response_json)

            except Exception as e:
                error_message = json.dumps({"error": f"Invalid data: {str(e)}"})
                await websocket.send_text(error_message)
                print(f"Error processing data: {e}")

    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await websocket.close()
        print("WebSocket connection closed")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
