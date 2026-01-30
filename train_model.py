import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# Dummy training data (replace this with real fire data later)
data = pd.DataFrame({
    'Temperature': [30, 35, 40, 20, 25, 38, 15, 32],
    'Humidity':    [50, 45, 30, 60, 55, 35, 70, 42],
    'WindSpeed':   [10, 15, 20,  5, 12, 25,  3, 14],
    'Dryness':     [ 7,  8,  9,  3,  4, 10,  2,  6],
    'Risk':        [ 1,  2,  2,  0,  1,  2,  0,  1]  # 0 = Low, 1 = Moderate, 2 = High
})

print("Training model...")  # Add a print statement here to confirm the script is running

# Train the model
X = data[['Temperature', 'Humidity', 'WindSpeed', 'Dryness']]
y = data['Risk']
model = RandomForestClassifier()
model.fit(X, y)

print("Model trained!")  # Another print statement to confirm training

# Save the model
os.makedirs('model', exist_ok=True)  # Ensure 'model' folder exists
with open('model/model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved to model/model.pkl")  # Confirm the model was saved
