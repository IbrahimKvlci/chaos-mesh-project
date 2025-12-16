from flask import Flask, jsonify

app = Flask(__name__)

products = [
    {'id': 1, 'name': 'Laptop', 'price': 999.99},
    {'id': 2, 'name': 'Smartphone', 'price': 499.99},
    {'id': 3, 'name': 'Headphones', 'price': 79.99}
]

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'product-service'}), 200

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({'products': products}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
