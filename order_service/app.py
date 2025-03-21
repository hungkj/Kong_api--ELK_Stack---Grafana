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

if __name__ == '__main__':
    app.run(port= 5001, host="0.0.0.0" ,debug=True)