from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Variables to store the latest sensor values and LED status
latest_temperature = None
latest_humidity = None
led_status = False  # LED is initially off

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

@app.route('/led', methods=['POST'])  # Endpoint for toggling LED state
def toggle_led():
    global led_status
    try:
        data = request.get_json()  # Get JSON data from the request
        if 'status' not in data:
            return jsonify({"error": "LED status not specified"}), 400
        
        # Update the LED status based on the received data
        led_status = True if data['status'] == 'on' else False
        
        return jsonify({"status": "success", "led_state": "on" if led_status else "off"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return the exception message

if __name__ == '__main__':
    app.run(debug=True)
