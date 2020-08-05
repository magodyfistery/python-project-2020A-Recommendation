from flask import Flask, redirect, url_for, request, json, session
from flask import render_template  # cargar html
import matplotlib


app = Flask(__name__)


@app.route("/")
def show_home():
    # user_data = json.loads(session['user_data'])

    return render_template("module_home/index.html", logged_in=False, user="Magody")


@app.route("/login")
def login():
    return "Pendiente programar"


@app.route("/register")
def register():
    return render_template("module_account/register.html")


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
    # TODO: GUARDAR DATOS
    session['user_data'] = json.dumps({"name": data['name']})  # cookie de sesión
    return redirect(url_for('.show_home'))


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
