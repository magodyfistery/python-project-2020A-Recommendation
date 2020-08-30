import json

from flask import Blueprint, session, render_template

from database import Database
from matrix_factorization_system.recommendations import user_candidate_generation, get_total_sources, grs
from models.category import Category
from models.product import Product


connection = Database.getConnection()
home_page = Blueprint('home_page', __name__, template_folder='templates')


@home_page.route("/")
def show_home():
    user_data = session.get('user_data', None)
    logged_in = session.get('logged_in', False)

    if logged_in:
        user = json.loads(user_data)

        user_id = user['id']
        quantity_recommendations = 6
        with_rated = False
        print("User id para recomendaciones", user_id)
        candidate_generation = user_candidate_generation(user_id, "id", "id_product")
        total_sources = get_total_sources(candidate_generation, user_id, with_rated=with_rated, verbosity=1)
        # las recomendaciones ya vienen ordenadas del mayor puntaje al menor
        recp = total_sources[0:quantity_recommendations]  # Aquí se enviará la lista de productos de recomendaciones personalizadas.
        res = grs(user_id)
        if res:
            recg = res
        else:
            recg = Product.select_best_sellers(connection, 6)
        #recg = Product.select_best_sellers(connection, 6) # Aquí se enviará la lista de productos de recomendaciones por grupo.
        return render_template("module_home/index.html",
                            logged_in=logged_in,
                            user=user,
                            categories=Category.select_categories(connection),
                            prods=Product.select_best_sellers(connection, 3),
                            topr=Product.select_top_rated(connection,5),
                            recp=recp,
                            recg = recg,
                            cat = Category.get_user_top_category(connection,json.loads(user_data)['username'])
                            )
    else:
        return render_template("module_home/index.html",
                            logged_in=logged_in,
                            categories=Category.select_categories(connection),
                            prods=Product.select_best_sellers(connection, 3),
                            topr=Product.select_top_rated(connection,5),
                            )

