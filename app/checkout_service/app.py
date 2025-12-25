import requests
import time
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'checkout-service'}), 200

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    # Mock checkout logic
    amount = 100.0 # Mock amount
    

    payment_service_url = os.environ.get('PAYMENT_SERVICE_URL', 'http://payment-service:5003')
    auth_service_url = os.environ.get('AUTH_SERVICE_URL', 'http://auth-service:5001')

    # Check Auth Service
    try:
        auth_response = requests.get(f'{auth_service_url}/health')
        if auth_response.status_code != 200:
             return jsonify({'error': 'Auth service unhealthy'}), 503
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Auth service unreachable'}), 503

    start_time = time.time()
    try:
        payment_response = requests.post(f'{payment_service_url}/pay', json={'amount': amount})
        payment_data = payment_response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Payment service unreachable', 'details': str(e)}), 503
    end_time = time.time()
    
    response_time = end_time - start_time

    if response_time > 4:
        return jsonify({'error': 'Payment processing timed out', 'details': 'Response time: ' + str(response_time)}), 504
    
    return jsonify({
        'status': 'success',
        'message': 'Checkout processed successfully',
        'order_id': 'order-12345',
        'payment_response': payment_data,
        'payment_response_time': response_time
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
