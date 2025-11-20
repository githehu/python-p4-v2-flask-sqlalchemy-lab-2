# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

# Initialize the database object
db = SQLAlchemy()

# --- Task #1: Add Review and relationships with Customer and Item ---

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    
    # Foreign Keys
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    
    # Relationships
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    # --- Task #3: Add Serialization ---
    serialize_rules = (
        '-customer.reviews', # Exclude recursion from Customer model
        '-item.reviews',     # Exclude recursion from Item model
    )

    def __repr__(self):
        return f'<Review {self.id}, Customer: {self.customer_id}, Item: {self.item_id}>'

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    # Relationships
    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete-orphan')

    # --- Task #2: Add Association Proxy ---
    # Get a list of items through the customer's reviews
    items = association_proxy('reviews', 'item')

    # --- Task #3: Add Serialization ---
    serialize_rules = (
        '-reviews.customer', # Exclude recursion from Review model
        '-items',            # Exclude items list in the base serialization to prevent deep nesting
    )

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    
    # Relationships
    reviews = db.relationship('Review', back_populates='item', cascade='all, delete-orphan')
    
    # Association Proxy (Optional, but could be useful: customers who reviewed this item)
    customers = association_proxy('reviews', 'customer')

    # --- Task #3: Add Serialization ---
    serialize_rules = (
        '-reviews.item', # Exclude recursion from Review model
        '-customers',    # Exclude customers list in the base serialization
    )

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'