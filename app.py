
import json

from flask import Flask, request, jsonify

from blueprints.blueprint_cart import cart_page
from blueprints.blueprint_home import home_page
from blueprints.blueprint_login import login_page
from blueprints.blueprint_my_account import my_account_page
from blueprints.blueprint_register import register_page
from blueprints.blueprint_product import product
from database import Database
from models.city import City
from matrix_factorization_system.recommendations import user_recommendations
from matrix_factorization_system.build_model import generateModel



connection = Database.getConnection()


app = Flask(__name__)
# forma de dividir la aplicación en partes
app.register_blueprint(home_page)
app.register_blueprint(login_page)
app.register_blueprint(register_page)
app.register_blueprint(cart_page)
app.register_blueprint(my_account_page)
app.register_blueprint(product)


model = None
id_items = None




@app.route('/api/get_cities')  # si se usa por más de un blueprint, debería estar en app.py
def get_cities():
    # print(request.args)
    id_country = request.args.get('id_country', 'default_if_none')
    cities = City.select_cities_from_country(connection, id_country)
    output = {'cities': [json.loads(city.toJSON()) for city in cities]}
    return jsonify(output)






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

    recommendations = user_recommendations(user_id, "id", "id_product", k=quantity_recommendations)

    arreglo = []
    for id in recommendations:
        arreglo.append(int(id))

    print(arreglo)

    respuesta = {
        'error': "",
        "body": {
            "status": 999,
            "msg": "Testeando %i recomendaciones para el usuario con id %i" % (quantity_recommendations, user_id),
            "data": arreglo
        }
    }



    return jsonify(respuesta)

if __name__ == "__main__":
    # generateModel()

    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.debug = True  # detecta cambios
    app.run()


