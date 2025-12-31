# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Product, CartItem
from forms import RegisterForm, LoginForm, ProductForm, ProfileForm, Order, OrderItem
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-for-development')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 限制文件大小为 5MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    products = Product.query.order_by(Product.created_at.desc()).all()  # 获取所有商品
    return render_template('index.html', products=products)  # 传给模板

@app.route('/user_center')
@login_required
def user_center():
    return render_template('user_center.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        if User.query.filter_by(username=username).first():
            flash('用户名已存在，请换一个。')
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash('注册成功！请登录。')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误。')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('您没有权限访问管理后台。', 'danger')
        return redirect(url_for('index'))
    
    users = User.query.all()
    products = Product.query.all()
    return render_template('admin.html', users=users, products=products)

@app.route('/admin/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        flash('权限不足！', 'danger')
        return redirect(url_for('index'))

    form = ProductForm()
    if form.validate_on_submit():
        file = form.image.data
        if file and allowed_file(file.filename):
            # 安全保存文件
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # 保存到数据库（使用相对路径）
            product = Product(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                image_url=f"uploads/{filename}"  # 存储相对路径
            )
            db.session.add(product)
            db.session.commit()

            flash('商品添加成功！', 'success')
            return redirect(url_for('admin'))
        else:
            flash('图片格式不支持，请上传 jpg/png/gif 文件。', 'danger')

    return render_template('add_product.html', form=form)

@app.route('/admin/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if not current_user.is_admin:
        flash('权限不足！', 'danger')
        return redirect(url_for('index'))

    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)  # 自动填充表单数据

    if form.validate_on_submit():
        # 更新字段
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data

        # 处理图片上传（如果上传了新图）
        file = form.image.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            product.image_url = f"uploads/{filename}"  # 更新路径

        db.session.commit()
        flash('商品更新成功！', 'success')
        return redirect(url_for('admin'))

    return render_template('edit_product.html', form=form, product=product)

@app.route('/admin/delete_product/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    if not current_user.is_admin:
        flash('权限不足！', 'danger')
        return redirect(url_for('index'))

    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('商品删除成功！', 'success')
    return redirect(url_for('admin'))

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    
    # 查找是否已有该商品在购物车中
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'已将 {product.name} 加入购物车！', 'success')
    return redirect(url_for('index'))

@app.route('/cart')
@login_required
def cart():
    items = current_user.cart_items
    total = sum(item.product.price * item.quantity for item in items)
    return render_template('cart.html', items=items, total=total)

@app.route('/update_cart/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        abort(403)
    
    quantity = int(request.form.get('quantity', 1))
    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    if cart_item.user_id == current_user.id:
        db.session.delete(cart_item)
        db.session.commit()
        flash('商品已从购物车移除', 'info')
    return redirect(url_for('cart'))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)  # 自动填充当前用户数据

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('个人信息已更新！', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html', form=form)

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = current_user.cart_items
    if not cart_items:
        flash('购物车为空，无法结算！', 'warning')
        return redirect(url_for('cart'))

    # 计算总价
    total = sum(item.product.price * item.quantity for item in cart_items)

    # 创建订单
    order = Order(user_id=current_user.id, total_price=total)
    db.session.add(order)
    db.session.flush()  # 获取 order.id

    # 创建订单明细 & 快照价格
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price  # 快照当前价格
        )
        db.session.add(order_item)

    # 清空购物车
    for item in cart_items:
        db.session.delete(item)

    db.session.commit()
    flash(f'订单创建成功！订单号：{order.id}，总价：¥{total:.2f}', 'success')
    return redirect(url_for('order_success', order_id=order.id))

@app.route('/order/success/<int:order_id>')
@login_required
def order_success(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('order_success.html', order=order)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(is_admin=True).first():
            admin = User(
                username='admin',
                email='admin@example.com',
                password=generate_password_hash('admin123', method='pbkdf2:sha256'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ 默认管理员账号已创建：admin / admin123")

    app.run(debug=True)