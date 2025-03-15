import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Sample numerical data (Replace this with actual training data)
data = {
    "cpu_usage": [10, 50, 80, 30, 60, 90],
    "memory_usage": [5, 40, 75, 25, 55, 85],
    "disk_usage": [15, 45, 70, 20, 50, 80],
    "network_bytes": [1000, 5000, 8000, 3000, 6000, 9000],
    "network_packets": [50, 200, 300, 100, 250, 400]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Initialize StandardScaler
scaler = StandardScaler()

# Fit the scaler on the dataset
scaler.fit(df)

# Save the scaler to a .pkl file
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("✅ Scaler saved successfully as 'scaler.pkl'.")
