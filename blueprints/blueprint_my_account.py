import json

from flask import Blueprint, session, render_template, request, flash, url_for
from werkzeug.utils import redirect

from database import Database
from models.country import Country
from models.user import User
from utils.cryptography import encrypt_with_sha_256

my_account_page = Blueprint('my_account_page', __name__, template_folder='templates')
connection = Database.getConnection()

@my_account_page.route("/my_account")
def my_account():
    user_data = session.get('user_data', None)
    return render_template("module_account/my_account.html",
                           logged_in=True,
                           user=json.loads(user_data) if user_data else None)


@my_account_page.route("/my_account/settings")
def my_account_settings():
    user_data = session.get('user_data', None)
    return render_template("module_account/settings.html",
                           countries=Country.select_countries(connection),
                           logged_in=True,
                           user=json.loads(user_data) if user_data else None)


@my_account_page.route('/api/update_user', methods=['POST'])
def update_user():
    data = request.form

    user_data = json.loads(session['user_data'])

    user = User(
            data['username'], data['name'], int(data['country']),
            data['city'], data['email'], user_data['passwd']
        )

    if encrypt_with_sha_256(data['password']) == user_data['passwd'] and data['password'] == data['password_confirmation']:
        if user.update(connection):
            session['user_data'] = user.toJSON()
            flash("User updated successfully")
            return redirect("/my_account")
        else:
            flash("Can't update user")
    else:
        flash("Exist a problem with the password")

    return redirect(url_for('.my_account_settings'))

