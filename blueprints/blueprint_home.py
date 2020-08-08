import json

from flask import Blueprint, session, render_template

from database import Database
from models.category import Category
from models.product import Product


connection = Database.getConnection()
home_page = Blueprint('home_page', __name__, template_folder='templates')


@home_page.route("/")
def show_home():
    user_data = session.get('user_data', None)
    logged_in = session.get('logged_in', False)
    return render_template("module_home/index.html",
                            logged_in=logged_in,
                            user=json.loads(user_data) if user_data else None,
                            categories=Category.select_categories(connection),
                            prods=Product.select_best_sellers(connection, 3),
                            topr=Product.select_top_rated(connection,5)
                            )