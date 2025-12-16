from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'payment-service'}), 200

@app.route('/pay', methods=['POST'])
def process_payment():
    data = request.json
    amount = data.get('amount')
        
    return jsonify({
            'status': 'success', 
            'message': 'Payment processed successfully', 
            'amount': amount
        }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
