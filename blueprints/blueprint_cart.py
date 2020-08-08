from flask import Blueprint

cart_page = Blueprint('cart_page', __name__, template_folder='templates')


@cart_page.route("/my_cart")
def my_cart():
    return "Pendiente programar"
