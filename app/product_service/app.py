from flask import Flask, jsonify
import time

app = Flask(__name__)

products = [
    {'id': 1, 'name': 'Laptop', 'price': 999.99, 'replaced': False},
    {'id': 2, 'name': 'Smartphone', 'price': 499.99, 'replaced': False},
    {'id': 3, 'name': 'Headphones', 'price': 79.99, 'replaced': False}
]


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'product-service'}), 200


@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({'products': products}), 200

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    for product in products:
        if product['id'] == product_id:
            return jsonify(product), 200
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
