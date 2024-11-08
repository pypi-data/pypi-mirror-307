from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample product data
products = [
    {"id": 1, "name": "Product A", "price": 9.99},
    {"id": 2, "name": "Product B", "price": 14.99},
    {"id": 3, "name": "Product C", "price": 19.99}
]

# GET all products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

# GET single product
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

# POST new product
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_product = {
        'id': len(products) + 1,
        'name': data['name'],
        'price': data['price']
    }
    products.append(new_product)
    return jsonify(new_product), 201

# PUT update product
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'name' in data:
        product['name'] = data['name']
    if 'price' in data:
        product['price'] = data['price']
    
    return jsonify(product)

# DELETE product
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    products.remove(product)
    return jsonify({'message': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)


#GET
# curl http://localhost:5000/products
#POST
#curl -X POST http://127.0.0.1:5000/products -H 'Content-Type: application/json' -d '{"name": "Product D", "price": 24.99}'
#UPDATE:
#curl -X PUT http://localhost:5000/products/1 -H 'Content-Type: application/json' -d '{"name": "Updated Product A", "price": 29.99}'
#DELETE
#curl -X DELETE http://localhost:5000/products/1