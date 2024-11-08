from flask import Flask, jsonify, request

app = Flask(__name__)

products = [
    {"id": 1, "name": "Product A", "price": 9.99},
    {"id": 2, "name": "Product B", "price": 14.99},
    {"id": 3, "name": "Product C", "price": 19.99}
]

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    else:
        return jsonify({'error': 'Product not found'}), 404

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = {
        'id': len(products) + 1,
        'name': data['name'],
        'price': data['price']
    }
    products.append(new_product)
    return jsonify(new_product), 201

if __name__ == '__main__':
    app.run(debug=True)

# Open terminal: 
# python3 app.py 
# Open new terminal and: 
# curl http://localhost:5000/products 
# curl -X POST http://127.0.0.1:5000/products -H 'Content-Type: application/json' -d '{"name": "Product D", "price": 24.99}'
