from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest_temperature = None
latest_humidity = None
led_state = "off"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sensor-data', methods=['POST'])
def receive_sensor_data():
    global latest_temperature, latest_humidity
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        
        if temperature is None or humidity is None:
            return jsonify({"error": "Temperature or humidity value not found"}), 400
        
        latest_temperature = temperature
        latest_humidity = humidity
        
        return jsonify({"status": "success", "temperature": temperature, "humidity": humidity})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/sensor-data', methods=['GET'])
def get_sensor_data():
    if latest_temperature is None or latest_humidity is None:
        return jsonify({"sensor_value": "No data available"}), 404
    return jsonify({
        "temperature": latest_temperature,
        "humidity": latest_humidity
    })

@app.route('/led', methods=['GET', 'POST'])
def control_led():
    global led_state
    if request.method == 'GET':
        return jsonify({"led_state": led_state})
    elif request.method == 'POST':
        data = request.get_json()
        if data and "status" in data:
            led_state = data["status"]
            return jsonify({"status": "success", "led_state": led_state})
        else:
            return jsonify({"error": "Invalid data"}), 400

if __name__ == '__main__':
    app.run(debug=True)
