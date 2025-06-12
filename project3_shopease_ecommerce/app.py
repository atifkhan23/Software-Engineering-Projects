import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import db, User, Product, CartItem, Order, OrderItem
from utils import login_required, admin_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shopease-secret-key-456'
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "instance", "shopease.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'customer'  # Default role
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
        else:
            hashed_password = generate_password_hash(password)
            user = User(username=username, password=hashed_password, role=role)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Logged in successfully!', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin_products'))
            return redirect(url_for('index'))
        flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/products')
def products():
    category = request.args.get('category')
    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])
        user_id = session['user_id']
        product = Product.query.get_or_404(product_id)
        if product.stock < quantity:
            flash('Not enough stock available.', 'error')
        else:
            cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
            if cart_item:
                cart_item.quantity += quantity
            else:
                cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)
            db.session.commit()
            flash('Item added to cart.', 'success')
        return redirect(url_for('cart'))
    cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/cart/remove/<int:id>', methods=['POST'])
@login_required
def remove_from_cart(id):
    cart_item = CartItem.query.get_or_404(id)
    if cart_item.user_id != session['user_id']:
        flash('Unauthorized action.', 'error')
        return redirect(url_for('cart'))
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart.', 'success')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        user_id = session['user_id']
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        if not cart_items:
            flash('Your cart is empty.', 'error')
            return redirect(url_for('cart'))
        total = sum(item.product.price * item.quantity for item in cart_items)
        order = Order(user_id=user_id, total=total, date=datetime.now())
        db.session.add(order)
        db.session.commit()
        for item in cart_items:
            order_item = OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity)
            product = Product.query.get(item.product_id)
            product.stock -= item.quantity
            db.session.add(order_item)
            db.session.delete(item)
        db.session.commit()
        flash('Order placed successfully! Payment processed (simulated).', 'success')
        return redirect(url_for('orders'))
    cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total)

@app.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.date.desc()).all()
    return render_template('orders.html', orders=orders)

@app.route('/admin/products', methods=['GET', 'POST'])
@admin_required
def admin_products():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        category = request.form['category']
        product = Product(name=name, price=price, stock=stock, category=category)
        db.session.add(product)
        db.session.commit()
        flash('Product added.', 'success')
        return redirect(url_for('admin_products'))
    products = Product.query.all()
    return render_template('admin_products.html', products=products)

@app.route('/admin/products/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        product.category = request.form['category']
        db.session.commit()
        flash('Product updated.', 'success')
        return redirect(url_for('admin_products'))
    return render_template('admin_products.html', products=Product.query.all(), edit_product=product)

@app.route('/admin/products/delete/<int:id>', methods=['POST'])
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@admin_required
def admin_orders():
    orders = Order.query.order_by(Order.date.desc()).all()
    return render_template('admin_orders.html', orders=orders)

# REST API Endpoints
@app.route('/api/products', methods=['GET'])
def api_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price, 'stock': p.stock, 'category': p.category} for p in products])

@app.route('/api/cart', methods=['GET'])
@login_required
def api_cart():
    cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{'id': item.id, 'product': item.product.name, 'quantity': item.quantity} for item in cart_items])

@app.route('/api/orders', methods=['GET'])
@login_required
def api_orders():
    orders = Order.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{'id': o.id, 'total': o.total, 'date': o.date.isoformat()} for o in orders])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)