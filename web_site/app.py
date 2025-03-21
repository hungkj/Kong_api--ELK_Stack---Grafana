from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from dotenv import load_dotenv
from flask_pymongo import PyMongo
import os
from bson import ObjectId
load_dotenv() 

MONGO_URI = os.getenv("MONGO_URI")

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)
CORS(app)  # Allow the API to be consumed by any frontend app
#connect toi mongodb



client = MongoClient(MONGO_URI,tls=True, tlsAllowInvalidCertificates=True)
db = client["call_api"]  # Thay bằng tên database của bạn

#test

try:
     print("Danh sách collection:", db.list_collection_names())
     
except Exception as e:
    print("Lỗi kết nối:", e)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to my API!'})


@app.route('/products', methods=['GET'])
def get_products():
    products =db.products.find()
    product_list = []
    for product in products:
        product_list.append({
            'id': str(product['_id']),
            'name': product['name'],
            'price': product['price'],
            'image': product['image'],
            'stock': product['stock']
        })
    return jsonify(product_list)

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    order = {
        'name': data['name'],
        'phone': data['phone'],
        'address': data['address'],
        'products': data['products'],
        
        
    }
    result = db.orders.insert_one(order)
    return jsonify({'success': True, 'message': 'Order placed successfully!', 'order_id': str(result.inserted_id)})


@app.route('/payments', methods=['POST'])
def payment():
    data = request.json  
    order = db.orders.find_one({"_id": ObjectId(data['order_id'])})

    # Tạo danh sách sản phẩm theo format mong muốn
    product_details = [
        f"{item['name']} - {item['quantity']} x {item['price']} VND = {item['quantity'] * item['price']} VND"
        for item in order['products']
    ]

    total = sum(item['quantity'] * item['price'] for item in order['products'])

    # Chỉ lưu 3 dòng thông tin như trong hình
    payment = {
        'products': product_details,
        'total': f"Tổng tiền: {total} VND"
    }

    db.payments.insert_one(payment)

    return jsonify({'success': True, 'message': 'Payment successfully!', 'payment': payment})
    
    

if __name__ == '__main__':
    app.run(debug=True)