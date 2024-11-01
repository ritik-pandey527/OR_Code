from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Variable to store the latest sensor values
latest_temperature = None
latest_humidity = None

# Variable to track LED state
led_state = "off"  # Default state is "off"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sensor-data', methods=['POST'])  # Endpoint for receiving sensor data
def receive_sensor_data():
    global latest_temperature, latest_humidity
    try:
        data = request.get_json()  # Get JSON data from the request
        if data is None:
            return jsonify({"error": "No data provided"}), 400
        
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        
        if temperature is None or humidity is None:
            return jsonify({"error": "Temperature or humidity value not found"}), 400
        
        # Update the latest sensor values
        latest_temperature = temperature
        latest_humidity = humidity
        
        return jsonify({"status": "success", "temperature": temperature, "humidity": humidity})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return the exception message

@app.route('/sensor-data', methods=['GET'])  # Endpoint for fetching sensor data
def get_sensor_data():
    if latest_temperature is None or latest_humidity is None:
        return jsonify({"sensor_value": "No data available"}), 404
    return jsonify({
        "temperature": latest_temperature,
        "humidity": latest_humidity
    })

@app.route('/led', methods=['GET', 'POST'])  # Endpoint for controlling and fetching LED state
def control_led():
    global led_state
    if request.method == 'GET':
        # Return the current LED state
        return jsonify({"led_state": led_state})
    elif request.method == 'POST':
        data = request.get_json()
        if data and "led_state" in data:
            led_state = data["led_state"]
            return jsonify({"status": "success", "led_state": led_state})
        else:
            return jsonify({"error": "Invalid data"}), 400

if __name__ == '__main__':
    app.run(debug=True)
