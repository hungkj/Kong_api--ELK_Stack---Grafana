from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
app = Flask(__name__)
#connect toi mongodb
client = MongoClient(MONGO_URI,tls=True, tlsAllowInvalidCertificates=True)
db = client['call_api']  # Thay bằng tên database của bạn
print(db)
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to my API!'})

@app.route('/products', methods=['GET'])
def get_product():
    products = db.products.find()
    product_lists = []
    for product in products:
        product_lists.append({ 
            'id': str(product['_id']),
            'name': product['name'],
            'price': product['price'],
            'image': product['image'],
            'stock': product['stock']
        })
    return jsonify(product_lists)

@app.route('/orders', methods=['POST'])
def make_orders():
    data= request.json
    order = {
        'name': data['name'],
        'phone': data['phone'],
        'address': data['address'],
        'products': data['products']
    }
    db.orders.insert_one(order)
    return jsonify({'message': 'Order created successfully!'})
    
@app.route('/payments',methods=['POST'])
def make_payment():
    data = request.json
    payment = {
        'price': data['price'],
        'stock': data['stock']

        }
    total = payment['price'] * payment['stock']
    totals = {
        'total': total
    }
    db.payments.insert_one(totals)
    return jsonify({'message': 'Payment created successfully!'})



if __name__ == '__main__':
    app.run(port= 7000 ,debug=True)