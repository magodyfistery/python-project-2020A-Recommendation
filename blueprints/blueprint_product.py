import json

from flask import Blueprint, session, render_template, Flask, redirect, url_for, request, json
from database import Database
from models.product import Product

connection = Database.getConnection()
product = Blueprint('product', __name__, template_folder='templates')

@product.route("/product")
def get_product():
    if 'view' in request.args:
        id=request.args['view']
        product = Product.get_product(connection,id)
        return render_template("module_home/product.html", logged_in =False, product = product, similar=Product.select_similar_products(connection,product.id_product,product.id_category,1))

#@app.route("/search")
#def search_results():
#    if 'q' in request.args:
#        print(x)