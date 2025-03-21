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
    app.run(port= 5002, host="0.0.0.0" ,debug=True)