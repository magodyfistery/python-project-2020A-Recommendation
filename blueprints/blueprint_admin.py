import json
import os
from functools import wraps

from flask import Blueprint, redirect, url_for, session, render_template, request, flash, jsonify
from werkzeug.utils import secure_filename

from database import Database
from models.category import Category
from models.country import Country
from models.news import News
from models.order_details import OrderDetails
from models.orders import Order
from models.product import Product
from models.user import User
from parameters import Parameters
from utils.cryptography import encrypt_with_sha_256

connection = Database.getConnection()

admin_page = Blueprint('admin_page', __name__, template_folder='templates')


def admin_guard(func):
    @wraps(func)  # copia la información de la función
    def wrapper(*args, **kwargs):
        logged_in_admin = session.get('logged_in_admin', False)
        if logged_in_admin:
            return func(*args, **kwargs)
        else:
            return redirect("/admin")

    return wrapper


@admin_page.route("/admin")
def login():
    logged_in_admin = session.get('logged_in_admin', False)
    if logged_in_admin:
        return redirect("/admin/panel")
    else:
        user_data_admin = session.get('user_data_admin', None)  # de registro previo
        return render_template("module_admin/login.html",
                           user=json.loads(user_data_admin) if user_data_admin else None)






@admin_page.route('/api/auth_admin', methods=['POST'])
def auth_admin():
    data = request.form

    user = User(
            data['username'], '', '',
            '', '', data['password']
        )

    user.passwd = encrypt_with_sha_256(user.passwd)

    session['user_data_admin'] = user.toJSON()

    if user.authAndRetrieveAdmin(connection):
        session['user_data_admin'] = user.toJSON()
        session['logged_in_admin'] = True
        return redirect("/admin/panel")
    else:
        flash("User or password incorrect. Or you aren't an Admin!")
        return redirect(url_for('.login'))





@admin_page.route("/admin/panel")
@admin_guard
def show_panel():
    user_data_admin = session.get('user_data_admin', None)  # de registro previo
    return render_template("module_admin/panel.html",
                            user=json.loads(user_data_admin) if user_data_admin else None,
                           logged_in=True
                           )





@admin_page.route("/admin/log_out")
@admin_guard
def log_out():
    session['user_data_admin'] = None
    session['logged_in_admin'] = False
    return redirect("/admin")

@admin_page.route('/api/get_products', methods=['POST'])  # si se usa por más de un blueprint, debería estar en app.py
@admin_guard
def get_products():
    data = request.form
    skip_products = data['skip_products']
    step_products = data['step_products']
    products = Product.select_products(connection, skip_products, step_products)
    output = {'products': [json.loads(product.toJSON()) for product in products]}
    return jsonify(output)

@admin_page.route('/api/get_news', methods=['POST'])  # si se usa por más de un blueprint, debería estar en app.py
@admin_guard
def get_news():
    data = request.form
    skip_news = data['skip_news']
    step_news = data['step_news']
    news = News.select_news(connection, skip_news, step_news)
    output = {'news': [json.loads(new.toJSON()) for new in news]}
    return jsonify(output)

@admin_page.route('/api/get_orders', methods=['POST'])  # si se usa por más de un blueprint, debería estar en app.py
@admin_guard
def get_orders():
    data = request.form
    skip_orders = data['skip_orders']
    step_orders = data['step_orders']
    orders_details = OrderDetails.select_orders(connection, skip_orders, step_orders)
    output = {'orders_details': [json.loads(json.dumps(detail)) for detail in orders_details]}
    return jsonify(output)


@admin_page.route('/api/get_users', methods=['POST'])  # si se usa por más de un blueprint, debería estar en app.py
@admin_guard
def get_users():
    data = request.form
    skip_users = data['skip_users']
    step_users = data['step_users']
    users = User.select_users(connection, skip_users, step_users)
    output = {'users': [json.loads(json.dumps(user)) for user in users]}

    return jsonify(output)


@admin_page.route('/admin/panel/addProduct')
@admin_guard
def addProduct():

    return render_template("module_admin/add_product.html",
                           logged_in=True,
                           categories=Category.select_categories(connection)
                           )

@admin_page.route('/admin/panel/addNew')
@admin_guard
def addNew():
    data = request.form

    print(data)
    return render_template("module_admin/add_new.html",
                           logged_in=True,
                           categories=News.select_news_categories(connection)
                           )


@admin_page.route('/admin/panel/updateProduct/<int:id_product>/<int:id_category>/<string:name>/<regex("\d+(\.\d+)?"):price>/<regex(".*"):img_path>')
@admin_guard
def updateProduct(id_product, id_category, name, price, img_path):
    product = Product(id_product, id_category, name, price, img_path.replace('_-SEP-_', "/"), -1)

    return render_template("module_admin/update_product.html",
                           logged_in=True,
                           categories=Category.select_categories(connection),
                           product=product
                           )


@admin_page.route('/admin/panel/updateNew', methods=['GET', 'POST'])
@admin_guard
def updateNew():
    data = request.form

    print(data)


    return render_template("module_admin/update_new.html",
                           logged_in=True,
                           categories=News.select_news_categories(connection),
                           new=data
                           )


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Parameters.ALLOWED_EXTENSIONS

@admin_page.route('/api/add_product', methods=['GET', 'POST'])
@admin_guard
def saveProductInDatabase():

    data = request.form
    split_category = data['category'].split("-")
    id_category = int(split_category[0])
    category_name = split_category[1].lower()

    image_name = _save_image(request.files['image'], category_name)
    if image_name is None:
        return redirect(url_for('.addProduct'))
    else:
        producto = Product(-1, id_category, data['product_name'], data['price'], "images/" +category_name + "/" + image_name, 0)
        print(producto)
        if producto.create(connection):
            return redirect('/admin/panel')
        else:
            flash("Error while executing command to database")
            return redirect(url_for('.addProduct'))


@admin_page.route('/api/add_new', methods=['GET', 'POST'])
@admin_guard
def saveNewInDatabase():

    data = request.form
    split_category = data['category'].split("-")
    id_category = int(split_category[0])
    category_name = split_category[1].lower()

    new = News()

    if new.create(connection):
        return redirect('/admin/panel')
    else:
        flash("Error while executing command to database")
        return redirect(url_for('.addNew'))


@admin_page.route('/api/update_product', methods=['GET', 'POST'])
@admin_guard
def updateProductInDatabase():

    data = request.form
    split_category = data['category'].split("-")
    id_category = int(split_category[0])
    category_name = split_category[1].lower()

    producto = Product(data['id_product'], -1, None, -1, None, -1)

    if request.files['image'].filename == '':
        producto = Product(data['id_product'], id_category, data['product_name'], data['price'], None, 0)
    else:
        image_name = _save_image(request.files['image'], category_name)
        if image_name is None:
            return redirect(url_for('.updateProduct',
                                id_product=data['id_product'],
                                id_category=id_category,
                                name=data['product_name'],
                                price=data['price'],
                                img_path=data['img_path']))
        else:
            producto = Product(data['id_product'], id_category, data['product_name'], data['price'], "images/" +category_name + "/" + image_name, 0)

    if producto.update(connection):
        return redirect('/admin/panel')
    else:
        flash("Error while executing command to database")
        return redirect(url_for('.updateProduct',
                                id_product=data['id_product'],
                                id_category=id_category,
                                name=data['product_name'],
                                price=data['price'],
                                img_path=data['img_path']))



def _save_image(file, category_name):
    # check if the post request has the file part
    if 'image' not in request.files:
        flash('No file part')
        return None

    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        full_img_path = Parameters.UPLOAD_FOLDER + "/" + category_name + "/" + filename
        file.save(full_img_path)
        return filename
    return None



@admin_page.route('/admin/settings')
@admin_guard
def my_account_settings():
    user_data_admin = session.get('user_data_admin', None)

    return render_template("module_admin/settings.html",
                           countries=Country.select_countries(connection),
                           logged_in=True,
                           user=json.loads(user_data_admin) if user_data_admin else None)




@admin_page.route('/api/update_admin', methods=['POST'])
@admin_guard
def update_admin():
    data = request.form

    user_data_admin = json.loads(session['user_data_admin'])

    user = User(
            data['username'], data['name'], int(data['country']),
            data['city'], data['email'], user_data_admin['passwd']
        )

    if encrypt_with_sha_256(data['password']) == user_data_admin['passwd'] and data['password'] == data['password_confirmation']:
        if user.update(connection):
            session['user_data_admin'] = user.toJSON()
            flash("User updated successfully")
            return redirect("/admin/panel")
        else:
            flash("Can't update user")
    else:
        flash("Exist a problem with the password")

    return redirect(url_for('.my_account_settings'))



@admin_page.route('/admin/dashboard')
@admin_guard
def view_dashboard():
    bar_labels, bar_values = Product.select_ten_best_selled_products(connection)
    line_labels, line_values = Order.select_ten_last_days(connection)
    user_data_admin = session.get('user_data_admin', None)



    return render_template('module_admin/dashboard.html',

                           bar_max= max(bar_values),
                           bar_labels=bar_labels,
                           bar_values=bar_values,
                           line_max= max(line_values),
                           line_labels=line_labels,
                           line_values=line_values,
                           logged_in=True,
                           user=json.loads(user_data_admin) if user_data_admin else None
                           )

