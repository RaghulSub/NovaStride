import json

def process_data(data):
    """
    Processes security event data and returns a JSON response based on overallLabel.
    """
    try:
        # Extract relevant fields
        security_event = data.get("securityEvent", {})
        source_ip = security_event.get("sourceIPAddress", "0.0.0.0")
        attack_type = security_event.get("attackType", "None")
        network_attack_type = data.get("networkEvent", {}).get("attackType", "None")
        system_attack_type = data.get("systemEvent", {}).get("attackType", "None")

        # Determine prediction based on overallLabel
        overall_label = data.get("overallLabel", "Normal")
        prediction = "Anomalous" if overall_label.lower() == "abnormal" else "Normal"

        # Return JSON response
        return json.dumps({
            "source_ip": source_ip,
            "prediction": prediction,
            "attack_type": attack_type,
            "network_attack_type": network_attack_type,
            "system_attack_type": system_attack_type
        }, indent=4)

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)

# Example usage
sample_log = {
    "eventTime": "2025-03-11T06:45:00.123456Z",
    "eventSource": "aws.cloud",
    "eventName": "SecurityAndSystemEvent",
    "awsRegion": "us-east-1",
    "securityEvent": {
        "sourceIPAddress": "192.168.1.100",
        "destinationIPAddress": "10.0.0.20",
        "userAgent": "API/Client",
        "eventType": "AwsApiCall",
        "eventName": "ConsoleLogin",
        "responseElements": {
            "ConsoleLogin": "Success"
        },
        "label": "Normal",
        "attackType": "None"
    },
    "networkEvent": {
        "sourceIPAddress": "192.168.1.101",
        "destinationIPAddress": "10.0.0.25",
        "bytesTransferred": 50000,
        "packetsTransferred": 150,
        "status": "Normal Traffic",
        "label": "Normal",
        "attackType": "None"
    },
    "systemEvent": {
        "instanceId": "i-1234567890abcdef",
        "cpuUtilization": 25.5,
        "memoryUsage": 45.3,
        "diskUsage": 55.0,
        "status": "Stable",
        "label": "Normal",
        "attackType": "None"
    },
    "overallLabel": "Normal",
}

# Run the function and print the result
result = process_data(sample_log)
print(result)
