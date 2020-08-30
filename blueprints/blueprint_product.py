import json

from flask import Blueprint, session, render_template, Flask, redirect, url_for, request, json, jsonify
from database import Database
from models.product import Product
from models.category import Category
from models.user_product_rating import UserProductRating
from matrix_factorization_system.recommendations import user_candidate_generation, get_total_sources, grs
connection = Database.getConnection()
product = Blueprint('product', __name__, template_folder='templates')

#Revisar y mejorar el código de esta clase.
@product.route("/product")
def get_product():
    if 'view' in request.args:
        user_data = session.get('user_data', None)
        logged_in = session.get('logged_in', False)
        id=request.args['view']
        product = Product.get_product(connection,id)
        if logged_in:
            user = json.loads(user_data)
            user_id = user['id']
            quantity_recommendations = 6
            with_rated = False
            print("User id para recomendaciones", user_id)
            candidate_generation = user_candidate_generation(user_id, "id", "id_product")
            total_sources = get_total_sources(candidate_generation, user_id, with_rated=with_rated, verbosity=0)
            recp = total_sources[0:quantity_recommendations]  # Aquí se enviará la lista de productos de recomendaciones personalizadas.
            res = grs(user_id)
            if res:
                recg = res
            else:
                recg = Product.select_best_sellers(connection, 6)
            return render_template("module_home/product.html", logged_in =logged_in, 
                                user=json.loads(user_data) if user_data else None,
                                product = product,
                                recp=recp,
                                recg=recg,
                                similar=Product.select_similar_products(connection,product.id_product,product.id_category,3))
        else:
            return render_template("module_home/product.html", logged_in =logged_in, 
                                product = product,
                                similar=Product.select_similar_products(connection,product.id_product,product.id_category,3))
@product.route("/search")
def search_results():
    if 'q' in request.args:
        prods = Product.query(connection,request.args['q'],6)
        user_data = session.get('user_data', None)
        logged_in = session.get('logged_in', False)
        if logged_in:
            user = json.loads(user_data)
            user_id = user['id']
            quantity_recommendations = 6
            with_rated = False
            print("User id para recomendaciones", user_id)
            candidate_generation = user_candidate_generation(user_id, "id", "id_product")
            total_sources = get_total_sources(candidate_generation, user_id, with_rated=with_rated, verbosity=0)
            recp = total_sources[0:quantity_recommendations]  # Aquí se enviará la lista de productos de recomendaciones personalizadas.
            res = grs(user_id)
            if res:
                recg = res
            else:
                recg = Product.select_best_sellers(connection, 6)
            return render_template("module_home/search.html", 
                                    logged_in=logged_in, 
                                    prods= prods,
                                    user=json.loads(user_data) if user_data else None,
                                    recp=recp,
                                    recg=recg
                                    )
        else:
            return render_template("module_home/search.html", 
                                    logged_in=logged_in, 
                                    prods= prods,
                                    )

@product.route("/category/<name>")
def select_category(name):
    user_data = session.get('user_data', None)
    logged_in = session.get('logged_in', False)
    categories = Category.select_categories(connection)
    for x in categories:
	    if x.category_name == name:
		    c = x
    return render_template("module_home/category.html",
                            logged_in=logged_in,
                            categories=categories,
                            user=json.loads(user_data) if user_data else None,
                            c=c, prods = Product.select_category_products(connection,c.id_category))

@product.route("/rating", methods=["POST"])
def save_rating():
    user_data = session.get('user_data', None)
    user=json.loads(user_data)
    username = user['username']
    if request.method == "POST":
        done = UserProductRating.insert_product_rated(connection,UserProductRating(username,request.json['pid'],request.json['r'],0))
        if done:
            if Product.update_avg_rating(connection,request.json['pid']):
                return jsonify({'res':True})
            else:
                return jsonify({'res':False})
        else:
            return jsonify({'res':done})