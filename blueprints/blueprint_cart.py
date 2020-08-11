from flask import Blueprint, session, render_template, request, redirect, flash, url_for
from models.product import Product
from models.cart import Cart
from models.orders import Order
from models.order_details import OrderDetails
from database import Database
from datetime import datetime
import json

connection = Database.getConnection()
cart_page = Blueprint('cart_page', __name__, template_folder='templates')


@cart_page.route("/my_cart", methods=["POST","GET"])
def my_cart():
    user_data = session.get('user_data', None)
    user=json.loads(user_data)
    logged_in = session.get('logged_in', False)
    username = user['username']
    if request.method=="POST":
        try:
            product_id = request.form.get('product_id')
            quantity = request.form.get('quantity')
            product = Product.get_product(connection, product_id)
            if product_id and quantity:
                total = float(product.price) * float(quantity)
                if 'mycart' in session:
                    if username in session['mycart']:
                       if product_id in session['mycart'][username]:
                           flash("This item is already in your cart!")
                           return redirect(request.referrer)
                       else:
                           session['mycart'][username][product_id] = {'name': product.name, 'price': product.price, 'quantity':quantity,'total':total}
                           flash("Item added to cart!")
                           return redirect(request.referrer)
                    else:
                        session['mycart'][username] = { product_id:{'name': product.name, 'price': product.price, 'quantity':quantity,'total':total} }
                        flash("Item added to cart!")
                        return redirect(request.referrer)
                else:
                    session['mycart'] = { username:{ product_id:{'name': product.name, 'price': product.price, 'quantity':quantity,'total':total} } }
                    flash("Item added to cart!")
                    return redirect(request.referrer)
        except Exception as e:
            print(e)
        finally:
            return redirect(request.referrer)
    else:
        prods = []
        if not 'mycart' in session or not username in session['mycart']:
            return render_template("module_home/mycart.html",logged_in=logged_in,prods=prods,user=user,total=None)
        else:
            cart_products = session['mycart'][username]
            total = 0
            if cart_products:
                for k, v in cart_products.items():
                    total = total + float(v['total'])
                    prods.append(Cart(k,v['name'],v['quantity'],v['price'],v['total']))
            return render_template("module_home/mycart.html",logged_in=logged_in,prods=prods,user=user, total=total)

@cart_page.route("/mycart_pop", methods=["POST","GET"])
def pop_product():
    if request.method=="POST":
        session.modified = True
        user_data = session.get('user_data', None)
        user=json.loads(user_data)
        username = user['username']
        id = request.form.get('product_id')
        session['mycart'][username].pop(id)
        return redirect(url_for(".my_cart"))

@cart_page.route("/save_order", methods=["POST","GET"])
def save_order():
    user_data = session.get('user_data', None)
    user=json.loads(user_data)
    username = user['username']
    prods = []
    if request.method == "POST":
        total  = request.form.get('total')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        print(now)
        if Order.insert_order(connection,Order(0,username,now,total)):
            cart_products = session['mycart'][username]
            if cart_products:
                for k, v in cart_products.items():
                    prods.append(Cart(k,v['name'],v['quantity'],v['price'],v['total']))
                for prod in prods:
                    OrderDetails.insert_order_details(connection,OrderDetails(0,0,prod.id_product,prod.quantity,prod.total))
                flash('Compra registrada exitósamente!')
                session.modified = True
                session['mycart'].pop(username)
                return redirect(url_for(".my_cart"))
        else:
            flash("Error guardando la compra, inténtelo más tarde.")
            return redirect(request.referrer)