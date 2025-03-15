import json
import pickle
import ipaddress
import numpy as np
import pandas as pd

# Load the trained model, encoders, and scaler
with open("cloud_security_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Convert IP to integer
def ip_to_int(ip):
    try:
        return int(ipaddress.ip_address(ip))
    except ValueError:
        return 0  # Default for invalid IPs

def process_data(data):
    """
    Processes received security event data, predicts anomalies using the trained model,
    and returns JSON with IP addresses and detected security issues.
    """
    try:
        # Extract values safely
        source_ip = data.get("securityEvent", {}).get("sourceIPAddress", "0.0.0.0")
        attack_type = data.get("securityEvent", {}).get("attackType", "Unknown")
        network_attack_type = data.get("networkEvent", {}).get("attackType", "Unknown")
        system_attack_type = data.get("systemEvent", {}).get("attackType", "Unknown")
        network_bytes = data.get("networkEvent", {}).get("bytesTransferred", 0)
        network_packets = data.get("networkEvent", {}).get("packetsTransferred", 0)
        cpu_usage = data.get("systemEvent", {}).get("cpuUtilization", 0)
        memory_usage = data.get("systemEvent", {}).get("memoryUsage", 0)
        disk_usage = data.get("systemEvent", {}).get("diskUsage", 0)

        # Encode categorical features
        attack_type_encoded = label_encoders["security_attack_type"].transform([attack_type])[0] \
            if attack_type in label_encoders["security_attack_type"].classes_ else 0
        network_attack_type_encoded = label_encoders["network_attack_type"].transform([network_attack_type])[0] \
            if network_attack_type in label_encoders["network_attack_type"].classes_ else 0
        system_attack_type_encoded = label_encoders["system_attack_type"].transform([system_attack_type])[0] \
            if system_attack_type in label_encoders["system_attack_type"].classes_ else 0

        # Normalize numerical features
        numeric_features = np.array([[cpu_usage, memory_usage, disk_usage, network_bytes, network_packets]])
        normalized_features = scaler.transform(numeric_features)

        # Prepare input features
        features = np.hstack((
            [ip_to_int(source_ip)],
            [attack_type_encoded, network_attack_type_encoded, system_attack_type_encoded],
            normalized_features.flatten()
        ))

        # Predict using the trained model
        prediction = model.predict([features])[0]

        # Return JSON response
        return json.dumps({
            "source_ip": source_ip,
            "prediction": "Anomalous" if prediction == 1 else "Normal",
            "attack_type": attack_type,
            "network_attack_type": network_attack_type,
            "system_attack_type": system_attack_type
        }, indent=4)

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)
sample_log = {
    "securityEvent": {
        "sourceIPAddress": "192.168.1.10",
        "attackType": "DDoS"
    },
    "networkEvent": {
        "attackType": "Port Scan",
        "bytesTransferred": 2048,
        "packetsTransferred": 50
    },
    "systemEvent": {
        "attackType": "Privilege Escalation",
        "cpuUtilization": 85.3,
        "memoryUsage": 70.5,
        "diskUsage": 60.2
    }
}

result = process_data(sample_log)

# Print the result
print(result)
