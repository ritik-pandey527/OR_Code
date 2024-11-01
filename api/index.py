from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Variable to store the latest sensor value
latest_sensor_value = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'there')
    greeting_message = f"Hello, {name}!"
    return jsonify({"message": greeting_message})

@app.route('/sensor-data', methods=['POST'])  # Endpoint for receiving sensor data
def receive_sensor_data():
    global latest_sensor_value
    try:
        data = request.get_json()  # Get JSON data from the request
        if data is None:
            return jsonify({"error": "No data provided"}), 400
        sensor_value = data.get('sensor_value')
        if sensor_value is None:
            return jsonify({"error": "No sensor value found"}), 400
        
        # Update the latest sensor value
        latest_sensor_value = sensor_value
        
        return jsonify({"status": "success", "sensor_value": sensor_value})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return the exception message

@app.route('/sensor-data', methods=['GET'])  # Endpoint for fetching sensor data
def get_sensor_data():
    if latest_sensor_value is None:
        return jsonify({"sensor_value": "No data available"}), 404
    return jsonify({"sensor_value": latest_sensor_value})

if __name__ == '__main__':
    app.run(debug=True)
