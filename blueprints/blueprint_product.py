import json

from flask import Blueprint, session, render_template, Flask, redirect, url_for, request, json
from database import Database
from models.product import Product
from models.category import Category

connection = Database.getConnection()
product = Blueprint('product', __name__, template_folder='templates')

@product.route("/product")
def get_product():
    if 'view' in request.args:
        id=request.args['view']
        product = Product.get_product(connection,id)
        return render_template("module_home/product.html", logged_in =False, product = product, similar=Product.select_similar_products(connection,product.id_product,product.id_category,1))

@product.route("/search")
def search_results():
    if 'q' in request.args:
        prods = Product.query(connection,request.args['q'],6)
        return render_template("module_home/search.html", logged_in=False, prods= prods)

@product.route("/category/<name>")
def select_category(name):
    categories = Category.select_categories(connection)
    for x in categories:
	    if x.category_name == name:
		    c = x
    
    return render_template("module_home/category.html", categories=categories, c=c, prods = Product.select_category_products(connection,c.id_category))