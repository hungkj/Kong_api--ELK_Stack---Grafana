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


if __name__ == '__main__':
    app.run(port= 5003, host="0.0.0.0" ,debug=True)