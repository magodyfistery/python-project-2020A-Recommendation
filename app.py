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
from recommendations import RecommendationCustomSystem

connection = Database.getConnection()

app = Flask(__name__)
# forma de dividir la aplicación en partes
app.register_blueprint(home_page)
app.register_blueprint(login_page)
app.register_blueprint(register_page)
app.register_blueprint(cart_page)
app.register_blueprint(my_account_page)
app.register_blueprint(product)


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
        "user": "user1",
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
    user = request.json['user']
    quantity_recommendations = request.json['quantity_recommendations']

    recommendations = RecommendationCustomSystem.get_recommendations(user, quantity_recommendations)

    respuesta = {
        'error': "",
        "body": {
            "status": 999,
            "msg": "Testeando %i recomendaciones para %s" % (quantity_recommendations, user),
            "data": recommendations
        }
    }

    return jsonify(respuesta)


if __name__ == "__main__":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.debug = True  # detecta cambios
    app.run()
