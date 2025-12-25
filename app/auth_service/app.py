from flask import Flask, jsonify, request
import time

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'auth-service'}), 200

@app.route('/login', methods=['POST'])
def login():
    # Mock login
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username == 'admin' and password == 'password':
        return jsonify({'token': 'mock-token-12345', 'message': 'Login successful', 'timestamp': time.time()}), 200
    return jsonify({'message': 'Invalid credentials', 'timestamp': time.time()}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
