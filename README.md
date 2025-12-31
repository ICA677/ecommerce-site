# 电商平台实验项目

> 基于 Flask 的全功能在线购物系统  
> **学号**：202330450761
> **姓名**：蒋睿诚 

---

## 📌 项目简介

本项目是一个轻量级但功能完整的电子商务平台，使用 Python Flask 框架开发，支持用户注册登录、商品浏览、购物车管理、订单结算及管理员后台。适用于课程实验、毕业设计或小型商业场景原型。

**主要技术栈**：
- **后端**：Flask + Flask-Login + Flask-WTF + Flask-SQLAlchemy
- **数据库**：SQLite（无需额外配置）
- **前端**：Jinja2 模板 + Bootstrap 5
- **部署**：云服务器（如华为云 ECS）

---

## 🗂 项目结构说明
ecommerce-site/
├── app.py                 # 主应用入口，定义路由与业务逻辑
├── models.py              # 数据库模型（User, Product, CartItem 等）
├── forms.py               # WTForms 表单类（注册、登录、商品表单等）
├── requirements.txt       # Python 依赖列表
├── database.db            # SQLite 数据库文件（运行后自动生成）
├── README.md              # 本说明文件
│
├── static/
│   ├── uploads/           # 商品图片上传目录（自动创建）
│   └── style.css          # 自定义 CSS 样式（可选）
│
└── templates/
├── base.html          # 基础模板（导航栏、页脚）
├── index.html         # 首页（商品列表）
├── register.html      # 用户注册页
├── login.html         # 用户登录页
├── user_center.html   # 用户中心
├── profile.html       # 个人信息编辑
├── cart.html          # 购物车页面
├── product_detail.html# 商品详情页
├── add_product.html   # 管理员添加商品页
├── edit_product.html  # 管理员编辑商品页
├── admin.html         # 管理员后台（用户+商品管理）
└── order_success.html # 订单成功页

---

## 🔧 核心文件功能详解

### `app.py`
- 应用初始化：配置 `SECRET_KEY`、数据库 URI、上传路径等
- 路由定义：涵盖所有页面（首页、注册、登录、购物车、订单、管理后台等）
- 启动逻辑：首次运行时自动创建数据库和默认管理员账号（`admin / admin123`）
- 关键特性：
  - 用户认证（`@login_required`）
  - 管理员权限控制（`current_user.is_admin`）
  - 安全文件上传（限制格式与大小）

### `models.py`
定义 SQLAlchemy 数据模型：
- `User`：用户信息（含 `is_admin` 字段）
- `Product`：商品信息（名称、描述、价格、图片路径）
- `CartItem`：购物车项（关联用户与商品）
- `Order` / `OrderItem`：订单主表与明细表（支持价格快照）

### `forms.py`
基于 WTForms 的表单验证：
- `RegisterForm` / `LoginForm`：带邮箱格式校验（需安装 `email_validator`）
- `ProductForm`：商品表单（含文件上传字段）
- `ProfileForm`：用户资料编辑表单

### `templates/`
- 所有 HTML 页面均继承 `base.html`，保证风格统一
- 使用 Jinja2 语法动态渲染数据（如 `{{ products }}`, `{{ current_user }}`）
- 响应式设计，适配手机与电脑

### `static/uploads/`
- 商品图片存储目录
- 图片通过 `secure_filename()` 安全处理，防止路径穿越攻击
