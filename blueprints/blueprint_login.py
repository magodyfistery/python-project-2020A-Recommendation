import json

from flask import Blueprint, redirect, url_for, session, render_template, request, flash
from database import Database
from models.user import User
from utils.cryptography import encrypt_with_sha_256

connection = Database.getConnection()

login_page = Blueprint('login_page', __name__, template_folder='templates')


@login_page.route("/login")
def login():
    user_data = session.get('user_data', None)  # de registro previo
    return render_template("module_account/login.html",
                           user=json.loads(user_data) if user_data else None)


@login_page.route('/api/auth_user', methods=['POST'])
def auth_user():
    data = request.form

    user = User(
            data['username'], '', '',
            '', '', data['password']
        )

    user.passwd = encrypt_with_sha_256(user.passwd)

    session['user_data'] = user.toJSON()

    if user.authAndRetrieve(connection):
        session['user_data'] = user.toJSON()
        session['logged_in'] = True
        return redirect("/")
    else:
        flash("User or password incorrect")
        return redirect(url_for('.login'))


@login_page.route("/log_out")
def log_out():
    session['user_data'] = None
    session['logged_in'] = False
    return redirect("/")