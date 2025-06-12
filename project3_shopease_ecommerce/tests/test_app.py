import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app import app, db
from models import User, Product, CartItem

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_register(client):
    response = client.post('/register', data={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 302  # Redirect to login
    user = User.query.filter_by(username='testuser').first()
    assert user is not None

def test_add_to_cart(client):
    client.post('/register', data={'username': 'testuser', 'password': 'testpass'})
    client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
    product = Product(name='Test Product', price=10.0, stock=10, category='Test')
    db.session.add(product)
    db.session.commit()
    response = client.post('/cart', data={'product_id': product.id, 'quantity': '1'})
    assert response.status_code == 302
    cart_item = CartItem.query.filter_by(user_id=1).first()
    assert cart_item.quantity == 1