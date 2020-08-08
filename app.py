import json

from flask import Flask, request, jsonify

from blueprints.blueprint_cart import cart_page
from blueprints.blueprint_home import home_page
from blueprints.blueprint_login import login_page
from blueprints.blueprint_my_account import my_account_page
from blueprints.blueprint_register import register_page
from database import Database
from models.city import City

connection = Database.getConnection()

app = Flask(__name__)
# forma de dividir la aplicación en partes
app.register_blueprint(home_page)
app.register_blueprint(login_page)
app.register_blueprint(register_page)
app.register_blueprint(cart_page)
app.register_blueprint(my_account_page)


@app.route('/api/get_cities')  # si se usa por más de un blueprint, debería estar en app.py
def get_cities():
    # print(request.args)
    id_country = request.args.get('id_country', 'default_if_none')
    cities = City.select_cities_from_country(connection, id_country)
    output = {'cities': [json.loads(city.toJSON()) for city in cities]}
    return jsonify(output)


if __name__ == "__main__":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.debug = True  # detecta cambios
    app.run()

