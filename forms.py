# forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, FloatField, SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length, Email
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from datetime import datetime

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('注册')

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

class ProductForm(FlaskForm):
    name = StringField('商品名称', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('商品描述', validators=[DataRequired()])
    price = FloatField('价格', validators=[DataRequired(), NumberRange(min=0.01)])
    image = FileField('商品图片', validators=[
        FileRequired(message='请上传商品图片'),
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], message='只允许上传图片文件')
    ])
    submit = SubmitField('添加商品')

class ProfileForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(), 
        Length(min=3, max=20, message='用户名长度为3-20个字符')
    ])
    email = StringField('邮箱', validators=[
        DataRequired(), 
        Email(message='请输入有效的邮箱地址')
    ])
    submit = SubmitField('保存修改')

# 订单主表
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='待支付')  # 可扩展：已支付、已发货等
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('orders', lazy=True))

# 订单明细表
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # 快照价格（防止商品改价影响历史订单）

    order = db.relationship('Order', backref=db.backref('items', lazy=True))
    product = db.relationship('Product')