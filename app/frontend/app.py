from flask import Flask, jsonify,request
import requests
import time

import os

app = Flask(__name__)

AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL', 'http://auth-service:5001')
PRODUCT_SERVICE_URL = os.environ.get('PRODUCT_SERVICE_URL', 'http://product-service:5002')
CHECKOUT_SERVICE_URL = os.environ.get('CHECKOUT_SERVICE_URL', 'http://checkout-service:5004')

@app.route('/')
def index():
    try:
        # Check Auth Service Health
        auth_health = requests.get(f'{AUTH_SERVICE_URL}/health').json()
        
        # Check Product Service Health
        product_health = requests.get(f'{PRODUCT_SERVICE_URL}/health').json()
        
        # Get Products
        start_time = time.time()
        products_response = requests.get(f'{PRODUCT_SERVICE_URL}/products')
        response_time = time.time() - start_time
        
        products = products_response.json().get('products') if products_response.status_code == 200 else []
        
        notifications = []
        if response_time > 2.0: # Threshold for "high load"
             notifications.append("System is experiencing high load, please be patient.")

        for product in products:
            if product.get('replaced'):
                notifications.append(f"Warning: Price for {product['name']} has been replaced!")

        return jsonify({
            'frontend_status': 'running',
            'auth_service_health': auth_health,
            'product_service_health': product_health,
            'products_available': products,
            'notifications': notifications
        })
    except requests.exceptions.ConnectionError as e:
        return jsonify({'error': f'Service connection failed: {str(e)}'}), 503

@app.route('/checkout', methods=['POST'])
def checkout():
    try:
        checkout_response = requests.post(f'{CHECKOUT_SERVICE_URL}/checkout', json={})
        checkout_data = checkout_response.json()
        
        if checkout_response.status_code == 503 and 'Auth service' in checkout_data.get('error', ''):
             return jsonify({'error': 'Checkout failed: Auth service is down. Please try again later.'}), 503

        return jsonify(checkout_data), checkout_response.status_code
    except requests.exceptions.ConnectionError as e:
        return jsonify({'error': f'Service connection failed: {str(e)}'}), 503

@app.route('/products', methods=['GET'])
def get_products():
    try:
        products_response = requests.get(f'{PRODUCT_SERVICE_URL}/products')
        return jsonify(products_response.json()), products_response.status_code
    except requests.exceptions.ConnectionError as e:
        return jsonify({'error': f'Service connection failed: {str(e)}'}), 503

@app.route('/products/<product_id>',methods=['GET'])
def get_product_by_id(product_id):
    try:
        products_response = requests.get(f'{PRODUCT_SERVICE_URL}/products/{product_id}')
        if(products_response.json().get('replaced')):
            return jsonify({'error': 'Product price has been replaced', 'product': products_response.json()}),500
        return jsonify(products_response.json()), products_response.status_code
    except requests.exceptions.ConnectionError as e:
        return jsonify({'error': f'Service connection failed: {str(e)}'}), 503

@app.route('/login', methods=['POST'])
def login():
    try:
        data=request.json
        login_response = requests.post(f'{AUTH_SERVICE_URL}/login', json={'username': data['username'], 'password': data['password']})
        login_data = login_response.json()
        if(login_data['timestamp'] > time.time() + 1):
            return jsonify({'error': 'Time drift detected'}), 401
        return jsonify({'token': login_data['token'], 'message': 'Login successful','timestamp_auth': login_data['timestamp'], 'timestamp_front': time.time()}), 
        login_response.status_code
    except Exception as e:
        return jsonify({'error': f'Service connection failed: {str(e)}'}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
