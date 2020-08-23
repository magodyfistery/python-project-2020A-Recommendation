import json
import os
from functools import wraps

from flask import Blueprint, redirect, url_for, session, render_template, request, flash, jsonify
from werkzeug.utils import secure_filename

from database import Database
from models.order_details import OrderDetails
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
    print(users)
    output = {'users': [json.loads(json.dumps(user)) for user in users]}

    return jsonify(output)


@admin_page.route('/admin/panel/addProduct')
@admin_guard
def addProduct():

    return render_template("module_admin/add_product.html", logged_in=True)



@admin_page.route('/admin/panel/updateProduct/<int:id>')
@admin_guard
def updateProduct(id):

    return "test " + str(id)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Parameters.ALLOWED_EXTENSIONS

@admin_page.route('/api/add_product', methods=['GET', 'POST'])
@admin_guard
def saveProductInDatabase():

    print(request.files)

    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            flash('No file part')
            return redirect(url_for('.addProduct'))

        file = request.files['image']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            full_img_path = Parameters.UPLOAD_FOLDER + "/" + filename
            file.save(full_img_path)


            img_path = "images/" + filename

        return redirect(url_for('.addProduct'))






