import pytest
from flask_app.app import app, db, products_collection  # Import Flask app & db connection
from pymongo.errors import ConnectionFailure

# Test 1: Check if a POST request to /products returns 405 status code
def test_products_route_invalid_method():
    """
    This test checks the /products route returns a 405 status code
    when a POST request is sent, as it only accepts GET requests.
    """
    with app.test_client() as client:
        response = client.post('/products')  # Sending POST request instead of GET
        assert response.status_code == 405  # Expected code 405

# Test 2: Check MongoDB Read Operation (ping the db)
def test_mongodb_connection():
    """
    This test checks the Flask app can connect to MongoDB by performing a ping operation.
    If the db is reachable, the ping should succeed.
    """
    try:
        # Try to ping the MongoDB server to check the connection
        db.command('ping')  # Ping the db to verify connection
        success = True
    except ConnectionFailure:
        success = False
    assert success is True  # The connection should be successful

# Test 3: Test MongoDB Write Operation (Insert a product into the db)
def test_mongodb_write_operation():
    """
    This test checks a product document is inserted into the MongoDB collection
    and verifies its existence by querying the db.
    """
    product_data = {
        "name": "Test Product",
        "price": 19.99,
        "tag": "Test tag"
    }

    # Insert new product into collection
    result = products_collection.insert_one(product_data)

    # Query database to verify the product was inserted
    inserted_product = products_collection.find_one({"_id": result.inserted_id})

    # verify the inserted product is not None  
    assert inserted_product is not None, "The product shoould have been inserted into the database"

    # verify the data matches what was inserted    
    assert inserted_product["name"] == product_data["name"], "The product name does not match"
    assert inserted_product["price"] == product_data["price"], "The product price does not match"
    assert inserted_product["tag"] == product_data["tag"], "The product tag does not match"
