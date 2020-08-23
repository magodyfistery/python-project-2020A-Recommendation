

import json
from time import sleep

from flask import Flask, request, jsonify

from blueprints.blueprint_cart import cart_page
from blueprints.blueprint_home import home_page
from blueprints.blueprint_login import login_page
from blueprints.blueprint_my_account import my_account_page
from blueprints.blueprint_register import register_page
from blueprints.blueprint_product import product
from database import Database
from models.city import City
from matrix_factorization_system.recommendations import user_candidate_generation, get_total_sources
from matrix_factorization_system.build_model import generateModel
from blueprints.blueprint_admin import admin_page
import threading

from parameters import Parameters

connection = Database.getConnection()





app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Parameters.UPLOAD_FOLDER
# forma de dividir la aplicación en partes
app.register_blueprint(home_page)
app.register_blueprint(login_page)
app.register_blueprint(register_page)
app.register_blueprint(cart_page)
app.register_blueprint(my_account_page)
app.register_blueprint(product)
app.register_blueprint(admin_page)

model = None
id_items = None




@app.route('/api/get_cities')  # si se usa por más de un blueprint, debería estar en app.py
def get_cities():
    # print(request.args)
    id_country = request.args.get('id_country', 'default_if_none')
    cities = City.select_cities_from_country(connection, id_country)
    output = {'cities': [json.loads(city.toJSON()) for city in cities]}
    return jsonify(output)




# matrix = get_sparse_matrix_ratings() # matrix de ratings sin ser convertida atensor

@app.route('/api/recommendations/by_custom', methods=['POST'])
def get_custom_recommendations():
    """
    Recibe un JSON con el usuario del que tomar recomendaciones y la cantidad de recomendaciones
    {
        "user_id": 1,
        "quantity_recommendations": 10
    }
    :return: {
        "error": "",
        "body": {
            "status": 1,
            "msg": "Mensaje de servidor",
            "data": []
        }
    }
    """
    global model, id_items

    user_id = request.json['user']
    quantity_recommendations = request.json['quantity_recommendations']

    with_rated = False
    candidate_generation = user_candidate_generation(user_id, "id", "id_product")
    total_sources = get_total_sources(candidate_generation, user_id, with_rated=with_rated, verbosity=0)
    recommendations = list(total_sources.index)[0:quantity_recommendations]  # ya viene ordenado con prioridad




    respuesta = {
        'error': "",
        "body": {
            "status": 999,
            "msg": "Testeando %i recomendaciones para el usuario con id %i" % (quantity_recommendations, user_id),
            "data": recommendations
        }
    }



    return jsonify(respuesta)


def model_updater():
    global keep_training

    while keep_training:
        generateModel(
            embedding_dim=30,
            init_stddev=1,
            num_iterations=500,
            learning_rate=0.03,
            verbosity=0
        )

        sleep(1200)  # cada 20 minutos


if __name__ == "__main__":

    print("Iniciando programa")
    keep_training = False

    threading.Thread(target=model_updater).start()

    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    # app.debug = True  # detecta cambios
    app.run(debug=True, use_reloader=False)


