from flask import Flask, redirect, url_for, request, json, session, flash, jsonify
from flask import render_template  # cargar html

from database import Database
from models.category import Category
from models.city import City
from models.country import Country
from models.product import Product
from models.user import User

connection = Database.getConnection()
app = Flask(__name__)


@app.route("/")
def show_home():
    return render_template("module_home/index.html",
                           logged_in=False,
                           user="Magody",
                           categories=Category.select_categories(connection),
                           prods=Product.select_best_sellers(connection, 3)
                           )


@app.route("/login")
def login():
    return "Pendiente programar"


@app.route("/register")
def register():
    user_data = session.get('user_data', None)  # de registro previo
    print(user_data)
    return render_template("module_account/register.html",
                           countries=Country.select_countries(connection),
                           user=json.loads(user_data) if user_data else None)



@app.route("/my_cart")
def my_cart():
    return "Pendiente programar"


@app.route("/my_account")
def my_account():
    return "Pendiente programar"


@app.route("/log_out")
def log_out():
    return "Pendiente programar"






"""API"""


@app.route('/api/save_user', methods=['POST'])
def parse_request():
    data = request.form

    user = User(
            data['username'], data['name'], int(data['country']),
            data['city'], data['email'], data['password']
        )

    if data['password'] != data['password_confirmation']:
        flash("Password and confirmation password are diferent")
        session['user_data'] = user.toJSON()
        return redirect(url_for('.register'))
    else:
        session['user_data'] = json.dumps({"user": user})  # cookie de sesión
        return redirect(url_for('.show_home'))


@app.route('/api/get_cities')
def get_updated_settings():
    # print(request.args)
    id_country = request.args.get('id_country', 'default_if_none')
    cities = City.select_cities_from_country(connection, id_country)
    output = {'cities': [json.loads(city.toJSON()) for city in cities]}
    return jsonify(output)


# valida que corre por primera vez
if __name__ == "__main__":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.debug = True  # detecta cambios
    app.run()



"""

@app.route("/Hola/")
@app.route("/Hola/<name>")
def hello(name=None):
    return render_template("hello.html", name=name)  # mandar html
    # la variable que se manda responde a lo que esta en codigo
    # jinja en el html que recibe un nombre
    
    
@app.route("/post/<int:post_id>")  # http://127.0.0.1:5000/post/888
def mostrar_post(post_id):
    return "Post %d" % post_id


@app.route("/usuario/<username>")  # redirecciones!,multiples dir
@app.route("/user/<username>")
def mostrar_nombre_perfil(username):
    return "User %s" % username
    
return redirect("http://www.example.com", code=302)

return redirect(url_for('foo'))
"""
