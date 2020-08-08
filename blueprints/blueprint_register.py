import json

from flask import Blueprint, redirect, url_for, session, render_template, request, flash
from database import Database
from models.country import Country
from models.user import User
from utils.cryptography import encrypt_with_sha_256

connection = Database.getConnection()

register_page = Blueprint('register_page', __name__, template_folder='templates')


@register_page.route("/register")
def register():
    user_data = session.get('user_data', None)  # de registro previo
    return render_template("module_account/register.html",
                           countries=Country.select_countries(connection),
                           user=json.loads(user_data) if user_data else None)


@register_page.route('/api/save_user', methods=['POST'])
def save_user():
    data = request.form

    user = User(
            data['username'], data['name'], int(data['country']),
            data['city'], data['email'], data['password']
        )

    user.passwd = encrypt_with_sha_256(user.passwd)
    session['user_data'] = user.toJSON()

    if data['password'] == data['password_confirmation']:

        if user.register(connection):
            user.passwd = ""
            session['user_data'] = user.toJSON()
            session['logged_in'] = True
            return redirect("/")
        else:
            flash("Cant register user")
    else:
        flash("Password and confirmation password are diferent")

    return redirect(url_for('.register'))