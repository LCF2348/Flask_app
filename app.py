from flask import Flask, render_template
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

#connection
CONNECTION_STRING = os.getenv('MONGO_URI')

client = MongoClient(CONNECTION_STRING)
db = client.shop_db 
products_collection = db.products  

#routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/products')
def products():
    products = products_collection.find()
    return render_template('products.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)