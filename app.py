from flask import Flask, render_template, request
from datetime import datetime
import requests
import pickle

app = Flask(__name__)

WEATHER_API_KEY = "f05cb96998ba4986af382450261701"

# ===== 15 INDIAN FORESTS =====
FORESTS = {
    "Jim Corbett National Park": "Jim Corbett National Park, Uttarakhand",
    "Kaziranga National Park": "Kaziranga National Park, Assam",
    "Sundarbans Forest": "Sundarbans, West Bengal",
    "Gir Forest": "Gir National Park, Gujarat",
    "Bandipur Forest": "Bandipur National Park, Karnataka",
    "Ranthambore National Park": "Ranthambore National Park, Rajasthan",
    "Periyar National Park": "Periyar National Park, Kerala",
    "Nilgiri Biosphere Reserve": "Nilgiri Hills, Tamil Nadu",
    "Kanha National Park": "Kanha National Park, Madhya Pradesh",
    "Pench National Park": "Pench National Park, Madhya Pradesh",
    "Satpura Forest": "Satpura National Park, Madhya Pradesh",
    "Simlipal Forest": "Simlipal National Park, Odisha",
    "Dandeli Forest": "Dandeli Forest, Karnataka",
    "Nagarhole Forest": "Nagarhole National Park, Karnataka",
    "Valley of Flowers": "Valley of Flowers, Uttarakhand"
}

search_history = []
successful_alerts = 0

# ===== LOAD MODEL =====
with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

# ===== WEATHER =====
def get_weather(area):
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={area}"
    data = requests.get(url).json()
    if "error" in data:
        return None
    return {
        "temperature": data["current"]["temp_c"],
        "humidity": data["current"]["humidity"],
        "wind": data["current"]["wind_kph"] / 3.6
    }

# ===== PREDICTION =====
def predict_fire(weather):
    t, h, w = weather.values()
    dryness = (t / h) * w
    pred = model.predict([[t, h, w, dryness]])[0]
    return ["Low Risk", "Moderate Risk", "High Risk"][pred]

def explain(weather):
    t, h, w = weather.values()
    ts = min((t / 45) * 40, 40)
    hs = min(((100 - h) / 100) * 35, 35)
    ws = min((w / 15) * 25, 25)
    total = ts + hs + ws
    return {
        "temperature": round(ts / total * 100, 1),
        "humidity": round(hs / total * 100, 1),
        "wind": round(ws / total * 100, 1)
    }

# ===== ROUTES =====
@app.route("/")
def home():
    return render_template(
        "index.html",
        forests=FORESTS.keys(),
        recent=search_history[-5:][::-1]
    )

@app.route("/predict", methods=["POST"])
def predict():
    global successful_alerts

    forest = request.form.get("area")
    custom_location = request.form.get("custom_location")

    # Decide which input to use
    if custom_location:
        location = custom_location
        display_name = custom_location
    else:
        location = FORESTS.get(forest)
        display_name = forest

    weather = get_weather(location)
    if not weather:
        return "Invalid location", 400

    prediction = predict_fire(weather)
    explanation = explain(weather)

    if prediction == "High Risk":
        successful_alerts += 1

    entry = {
        "area": display_name,
        "temperature": round(weather["temperature"], 2),
        "humidity": round(weather["humidity"], 2),
        "wind": round(weather["wind"], 2),
        "prediction": prediction,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "explanation": explanation
    }

    search_history.append(entry)

    return render_template(
        "dashboard.html",
        latest=entry,
        prediction=prediction,
        explanation=explanation,
        success=successful_alerts
    )

if __name__ == "__main__":
    app.run(debug=True)
