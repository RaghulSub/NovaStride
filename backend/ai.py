import json
import pickle
import ipaddress
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Convert IP to Integer
def ip_to_int(ip):
    try:
        return int(ipaddress.ip_address(ip))
    except (ValueError, TypeError):
        return 0  # Default value for invalid or missing IPs

# Load JSON Data
with open("cloud_logs.json", "r") as f:
    data = json.load(f)

# Convert JSON to DataFrame
security_dataset = []
for entry in data:
    security_event = entry.get("securityEvent", {})
    
    security_dataset.append({
        "security_source_ip": ip_to_int(security_event.get("sourceIPAddress", "0.0.0.0")),
        "security_attack_type": security_event.get("attackType", "Unknown"),
        "label": entry.get("overallLabel", "Normal")  # Default to 'Normal' if missing
    })

# Convert to DataFrame
df = pd.DataFrame(security_dataset)

# Encode Categorical Data
label_encoders = {}
categorical_columns = ["security_attack_type"]
for col in categorical_columns:
    label_encoders[col] = LabelEncoder()
    df[col] = label_encoders[col].fit_transform(df[col])

# Split Data
X = df.drop(columns=["label"], errors='ignore')  # Ignore errors if column is missing
y = df.get("label", "Normal")  # Default to 'Normal' if missing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save Model, Encoders
with open("cloud_security_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("label_encoders.pkl", "wb") as f:
    pickle.dump(label_encoders, f)

print("✅ Security model trained and saved successfully.")
