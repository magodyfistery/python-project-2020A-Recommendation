import json

from flask import Blueprint, jsonify, request
from database import Database
from models.news import News

connection = Database.getConnection()

news_page = Blueprint('news_page', __name__, template_folder='templates')


@news_page.route("/api/news/<string:date_begin>", methods=["POST"])
def get_news_from_begin_date(date_begin):

    news = News.get_news_from_date(connection, date_begin)
    output = {'news': [json.loads(json.dumps(new)) for new in news]}

    return jsonify(output)


@news_page.route('/api/news_interact', methods=['GET', 'POST'])
def user_click_interact():

    id_news = request.args.get('id_news', 'default_if_none')
    username_user = request.args.get('username_user', 'default_if_none')

    return jsonify({'OK': News.add_interact_with_user(connection, id_news, username_user)})



