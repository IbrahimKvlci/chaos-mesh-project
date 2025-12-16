from flask import Flask, jsonify
import requests

import os

app = Flask(__name__)

AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL', 'http://localhost:5001')
PRODUCT_SERVICE_URL = os.environ.get('PRODUCT_SERVICE_URL', 'http://localhost:5002')
CHECKOUT_SERVICE_URL = os.environ.get('CHECKOUT_SERVICE_URL', 'http://localhost:5004')

@app.route('/')
def index():
    try:
        # Check Auth Service Health
        auth_health = requests.get(f'{AUTH_SERVICE_URL}/health').json()
        
        # Check Product Service Health
        product_health = requests.get(f'{PRODUCT_SERVICE_URL}/health').json()
        
        # Get Products
        products_response = requests.get(f'{PRODUCT_SERVICE_URL}/products')
        products = products_response.json().get('products') if products_response.status_code == 200 else []
        
        return jsonify({
            'frontend_status': 'running',
            'auth_service_health': auth_health,
            'product_service_health': product_health,
            'products_available': products
        })
    except requests.exceptions.ConnectionError as e:
        return jsonify({'error': f'Service connection failed: {str(e)}'}), 503

@app.route('/checkout', methods=['POST'])
def checkout():
    try:
        checkout_response = requests.post(f'{CHECKOUT_SERVICE_URL}/checkout', json={})
        checkout_data = checkout_response.json()
        return jsonify(checkout_data), checkout_response.status_code
    except requests.exceptions.ConnectionError as e:
        return jsonify({'error': f'Service connection failed: {str(e)}'}), 503


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
