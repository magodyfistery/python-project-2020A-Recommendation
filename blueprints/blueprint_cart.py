from flask import Blueprint, session, render_template, request, redirect, flash
from models.product import Product
from database import Database
import json

connection = Database.getConnection()
cart_page = Blueprint('cart_page', __name__, template_folder='templates')


@cart_page.route("/my_cart", methods=["POST","GET"])
def my_cart():
    user_data = session.get('user_data', None)
    user=json.loads(user_data)
    username = user['username']
    if request.method=="POST":
        try:
            product_id = request.form.get('product_id')
            quantity = request.form.get('quantity')
            product = Product.get_product(connection, product_id)
            if product_id and quantity:
                if 'mycart' in session:
                    if username in session['mycart']:
                       if product_id in session['mycart'][username]:
                           flash("This item is already in your cart!")
                           return redirect(request.referrer)
                       else:
                           session['mycart'][username][product_id] = {'name': product.name, 'price': product.price, 'quantity':quantity}
                           flash("Item added to cart!")
                           return redirect(request.referrer)
                    else:
                        session['mycart'][username] = { product_id:{'name': product.name, 'price': product.price, 'quantity':quantity} }
                        flash("Item added to cart!")
                        return redirect(request.referrer)
                else:
                    session['mycart'] = { username:{ product_id:{'name': product.name, 'price': product.price, 'quantity':quantity} } }
                    flash("Item added to cart!")
                    return redirect(request.referrer)
        except Exception as e:
            print(e)
        finally:
            return redirect(request.referrer)
