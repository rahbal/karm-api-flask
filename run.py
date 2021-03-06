from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init api
app = Flask(__name__)

app.config.from_pyfile('config.py')

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://testadmin:root@localhost/flask-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# Product class
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))

    def __init__(self, name, description):
        self.name = name
        self.description = description


# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description')


# Init Schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)


# Create a product
@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']

    new_product = Product(name, description)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


# Get all products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result.data)


# Get Single products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


# Update a product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']

    product.name = name
    product.description = description
    db.session.commit()

    return product_schema.jsonify(product)


# Delete product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)


app.config.from_pyfile('config.py')

# Run server
if __name__ == '__main__':
    app.run(debug=True)
