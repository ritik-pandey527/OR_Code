from flask import Flask, jsonify, request, render_template
from flask_cors import CORS  # Add this line to handle CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'there')
    greeting_message = f"Hello, {name}!"
    return jsonify({"message": greeting_message})

@app.route('/sensor-data', methods=['POST'])  # Endpoint for sensor data
def sensor_data():
    try:
        data = request.get_json()  # Get JSON data from the request
        if data is None:
            return jsonify({"error": "No data provided"}), 400
        sensor_value = data.get('sensor_value')
        if sensor_value is None:
            return jsonify({"error": "No sensor value found"}), 400
        
        # Process the sensor data as needed (e.g., store it in a database)
        
        return jsonify({"status": "success", "sensor_value": sensor_value})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return the exception message

if __name__ == '__main__':
    app.run(debug=True)
