"""
    Cart Service:
    Håndterer brugernes indkøbskurve.
    Tilbyder funktioner til at tilføje, fjerne og opdatere varer i kurven.
"""

from flask import Flask, jsonify, request
from cart import select_all_items, find_item_by_id, add_new_item, delete_item_by_id, update_amount
import requests

app = Flask(__name__)

# Get cart items
@app.route('/cart', methods=['GET'])
def get_cart_items():
    result = select_all_items()

    if result[0] == 200:
        cart_items = []
        for item in result[1]:
            product = get_product_by_id(item["product_id"])
            if product:
                cart_items.append({
                    "id": item["id"],
                    "product": product[0],
                    "amount": item["amount"]
                })

        result[1] = cart_items


    return jsonify(result[1]), result[0]

# Add a product to cart
@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    product = data.get('product_id')
    amount = data.get('amount')

    if not product:
        return jsonify({'message': 'At least one product is required'}), 400

    cart_item = {
        "product_id": product,
        "amount": amount if amount else 1,
    }

    result = add_new_item(cart_item)
    return jsonify(result[1]), result[0]

# Remove product from cart
@app.route('/cart/<int:id>', methods=['DELETE'])
def delete_item_from_cart(id):
    item = find_item_by_id(id)
    if item[0] == 200:
        result = delete_item_by_id(id)
        return jsonify(result[1]), result[0]
    
    return jsonify({'message': 'No item with specified id found'}), 404
    

# Update product amount
@app.route('/cart/<int:id>', methods=['PATCH'])
def update_product_amount(id):
    data = request.json
    amount = data.get('amount')

    if not amount:
        return jsonify({'message': 'Specifying amount is required'}), 400
    
    if amount == 0:
        delete_item_from_cart(id)
        return

    result = update_amount(id, amount)
    return jsonify(result[1]), result[0]

def get_product_by_id(id):
    url = f'http://product_catalog_service:5000/products/{id}'
    req = requests.get(url)
    if req.status_code == 200:
        return req.json()
    
    return None


app.run(debug=True, host='0.0.0.0', port=5001)