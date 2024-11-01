from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/greet', methods=['GET'])
def greet():
    # Check if a name is provided in the request arguments
    name = request.args.get('name', 'there')
    greeting_message = f"Hello, {name}!"
    
    # Return a JSON response with the greeting
    return jsonify({"message": greeting_message})

if __name__ == '__main__':
    app.run(debug=True)
