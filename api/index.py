from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'there')
    greeting_message = f"Hello, {name}!"
    return jsonify({"message": greeting_message})

@app.route('/sensor-data', methods=['POST'])  # New endpoint for sensor data
def sensor_data():
    data = request.get_json()  # Get JSON data from the request
    if data is None:
        return jsonify({"error": "No data provided"}), 400  # Return error if no data is sent
    sensor_value = data.get('sensor_value')  # Extract sensor value
    if sensor_value is None:
        return jsonify({"error": "No sensor value found"}), 400  # Return error if no sensor value

    # Process the sensor data as needed (e.g., store it in a database)
    
    return jsonify({"status": "success", "sensor_value": sensor_value})

if __name__ == '__main__':
    app.run(debug=True)
